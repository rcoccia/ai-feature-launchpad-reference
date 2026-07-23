using System.Data;
using System.Globalization;
using Microsoft.Data.Sqlite;

namespace Launchpad.Api;

internal enum DecisionKind
{
    ProductApproval,
    AiRiskApproval,
    Rejection,
}

internal sealed class LaunchpadStore(string databasePath)
{
    private const int SchemaVersion = 1;

    private static readonly HashSet<string> ExpectedObjects =
    [
        "table:audit_events",
        "table:launch_requests",
        "trigger:audit_events_no_delete",
        "trigger:audit_events_no_update",
        "trigger:audit_events_sequence_and_snapshot",
        "trigger:launch_requests_no_delete",
        "trigger:launch_requests_no_terminal_update",
    ];

    private readonly string _databasePath = Path.GetFullPath(databasePath);

    internal async Task InitializeAsync(CancellationToken cancellationToken = default)
    {
        var directory = Path.GetDirectoryName(_databasePath);
        if (!string.IsNullOrEmpty(directory))
        {
            Directory.CreateDirectory(directory);
        }

        await using var connection = await OpenConnectionAsync(cancellationToken);
        await ExecuteAsync(connection, null, "PRAGMA journal_mode=DELETE;", cancellationToken);
        using var transaction = connection.BeginTransaction(deferred: false);

        var version = Convert.ToInt32(
            await ScalarAsync(
                connection,
                transaction,
                "PRAGMA user_version;",
                cancellationToken),
            CultureInfo.InvariantCulture);
        var objects = await ReadSchemaObjectsAsync(connection, transaction, cancellationToken);

        if (version == 0)
        {
            if (objects.Count != 0)
            {
                throw new InvalidOperationException(
                    "Schema version 0 is accepted only for an empty SQLite store.");
            }

            await ExecuteAsync(connection, transaction, SchemaSql, cancellationToken);
            await ExecuteAsync(
                connection,
                transaction,
                $"PRAGMA user_version={SchemaVersion};",
                cancellationToken);
        }
        else if (version != SchemaVersion || !objects.SetEquals(ExpectedObjects))
        {
            throw new InvalidOperationException(
                $"SQLite schema is incomplete or unsupported (user_version={version}).");
        }

        transaction.Commit();
    }

    internal async Task<LaunchRequestResource> CreateAsync(
        string featureName,
        string requesterActorId,
        CancellationToken cancellationToken)
    {
        await using var connection = await OpenConnectionAsync(cancellationToken);
        using var transaction = connection.BeginTransaction(deferred: false);
        var id = Guid.NewGuid().ToString("D");
        var occurredAt = UtcNow();

        await ExecuteAsync(
            connection,
            transaction,
            """
            INSERT INTO launch_requests (
                id, feature_name, status, requester_actor_id, version,
                created_at_utc, updated_at_utc)
            VALUES ($id, $featureName, 'Pending', $requesterActorId, 0, $now, $now);
            """,
            cancellationToken,
            ("$id", id),
            ("$featureName", featureName),
            ("$requesterActorId", requesterActorId),
            ("$now", occurredAt));

        await AppendAuditAsync(
            connection,
            transaction,
            id,
            occurredAt,
            "Submit",
            requesterActorId,
            "Requester",
            "Succeeded",
            "request_created",
            "Pending",
            0,
            cancellationToken);

        var resource = await LoadRequiredAsync(
            connection,
            transaction,
            id,
            cancellationToken);
        transaction.Commit();
        return resource;
    }

    internal async Task<LaunchRequestResource?> GetAsync(
        string requestId,
        CancellationToken cancellationToken)
    {
        await using var connection = await OpenConnectionAsync(cancellationToken);
        using var transaction = connection.BeginTransaction(deferred: true);
        var resource = await LoadAsync(connection, transaction, requestId, cancellationToken);
        transaction.Commit();
        return resource;
    }

    internal async Task<AuditResource?> GetAuditAsync(
        string requestId,
        CancellationToken cancellationToken)
    {
        await using var connection = await OpenConnectionAsync(cancellationToken);
        using var transaction = connection.BeginTransaction(deferred: true);

        await using var featureCommand = CreateCommand(
            connection,
            transaction,
            "SELECT feature_name FROM launch_requests WHERE id = $id;",
            ("$id", requestId));
        var featureName = await featureCommand.ExecuteScalarAsync(cancellationToken) as string;
        if (featureName is null)
        {
            transaction.Commit();
            return null;
        }

        await using var command = CreateCommand(
            connection,
            transaction,
            """
            SELECT sequence, occurred_at_utc, action, actor_id, actor_role, outcome,
                   reason_code, status_after, version_after
            FROM audit_events
            WHERE request_id = $id
            ORDER BY sequence;
            """,
            ("$id", requestId));
        var events = new List<AuditEventResource>();
        {
            await using var reader = await command.ExecuteReaderAsync(cancellationToken);
            while (await reader.ReadAsync(cancellationToken))
            {
                events.Add(new AuditEventResource(
                    reader.GetInt32(0),
                    reader.GetString(1),
                    reader.GetString(2),
                    reader.IsDBNull(3) ? null : reader.GetString(3),
                    reader.IsDBNull(4) ? null : reader.GetString(4),
                    reader.GetString(5),
                    reader.GetString(6),
                    reader.GetString(7),
                    reader.GetInt32(8)));
            }
        }

        transaction.Commit();
        return new AuditResource(requestId, featureName, events);
    }

    internal async Task<DecisionResult> DecideAsync(
        string requestId,
        DecisionKind kind,
        ReferenceIdentity identity,
        CancellationToken cancellationToken)
    {
        await using var connection = await OpenConnectionAsync(cancellationToken);
        using var transaction = connection.BeginTransaction(deferred: false);
        var current = await LoadAsync(connection, transaction, requestId, cancellationToken);
        if (current is null)
        {
            transaction.Commit();
            return new(null, ApiContract.RequestNotFound());
        }

        var action = ActionName(kind);
        var suppliedRole = RoleName(identity.Role);

        if (identity.ActorProblem is not null)
        {
            return await RefuseAsync(
                connection,
                transaction,
                current,
                action,
                null,
                suppliedRole,
                WithRequest(identity.ActorProblem, requestId),
                cancellationToken);
        }

        if (identity.RoleProblem is not null)
        {
            return await RefuseAsync(
                connection,
                transaction,
                current,
                action,
                identity.ActorId,
                null,
                WithRequest(identity.RoleProblem, requestId),
                cancellationToken);
        }

        if (!RoleAuthorizes(identity.Role!.Value, kind))
        {
            return await RefuseAsync(
                connection,
                transaction,
                current,
                action,
                identity.ActorId,
                suppliedRole,
                ApiContract.RoleMismatch(requestId),
                cancellationToken);
        }

        if (current.Status is "Approved" or "Rejected")
        {
            return await RefuseAsync(
                connection,
                transaction,
                current,
                action,
                identity.ActorId,
                suppliedRole,
                ApiContract.RequestTerminal(requestId),
                cancellationToken);
        }

        var existingApproval = kind switch
        {
            DecisionKind.ProductApproval => current.Approvals.Product,
            DecisionKind.AiRiskApproval => current.Approvals.AiRisk,
            _ => null,
        };
        if (existingApproval is not null)
        {
            return await RefuseAsync(
                connection,
                transaction,
                current,
                action,
                identity.ActorId,
                suppliedRole,
                ApiContract.ApprovalAlreadyRecorded(requestId),
                cancellationToken);
        }

        if (kind is not DecisionKind.Rejection
            && identity.ActorId == current.RequesterActorId)
        {
            return await RefuseAsync(
                connection,
                transaction,
                current,
                action,
                identity.ActorId,
                suppliedRole,
                ApiContract.RequesterCannotApprove(requestId),
                cancellationToken);
        }

        var otherApprover = kind switch
        {
            DecisionKind.ProductApproval => current.Approvals.AiRisk?.ActorId,
            DecisionKind.AiRiskApproval => current.Approvals.Product?.ActorId,
            _ => null,
        };
        if (otherApprover is not null && identity.ActorId == otherApprover)
        {
            return await RefuseAsync(
                connection,
                transaction,
                current,
                action,
                identity.ActorId,
                suppliedRole,
                ApiContract.ApproversNotDistinct(requestId),
                cancellationToken);
        }

        var occurredAt = UtcNow();
        await ApplyDecisionAsync(
            connection,
            transaction,
            current,
            kind,
            identity.ActorId!,
            suppliedRole!,
            occurredAt,
            cancellationToken);
        var updated = await LoadRequiredAsync(
            connection,
            transaction,
            requestId,
            cancellationToken);
        await AppendAuditAsync(
            connection,
            transaction,
            requestId,
            occurredAt,
            action,
            identity.ActorId,
            suppliedRole,
            "Succeeded",
            kind == DecisionKind.Rejection ? "request_rejected" : "approval_recorded",
            updated.Status,
            updated.Version,
            cancellationToken);
        transaction.Commit();
        return new(updated, null);
    }

    internal static bool IsAvailabilityFailure(SqliteException exception) =>
        exception.SqliteErrorCode is 5 or 6 or 8 or 10 or 13 or 14;

    private async Task<SqliteConnection> OpenConnectionAsync(
        CancellationToken cancellationToken)
    {
        var connection = new SqliteConnection(
            new SqliteConnectionStringBuilder
            {
                DataSource = _databasePath,
                Mode = SqliteOpenMode.ReadWriteCreate,
                ForeignKeys = true,
                DefaultTimeout = 5,
            }.ToString());
        await connection.OpenAsync(cancellationToken);
        await ExecuteAsync(
            connection,
            null,
            """
            PRAGMA foreign_keys=ON;
            PRAGMA busy_timeout=5000;
            PRAGMA synchronous=FULL;
            """,
            cancellationToken);
        return connection;
    }

    private static async Task ApplyDecisionAsync(
        SqliteConnection connection,
        SqliteTransaction transaction,
        LaunchRequestResource current,
        DecisionKind kind,
        string actorId,
        string actorRole,
        string occurredAt,
        CancellationToken cancellationToken)
    {
        var sql = kind switch
        {
            DecisionKind.ProductApproval =>
                """
                UPDATE launch_requests
                SET product_approver_actor_id = $actorId,
                    product_approved_at_utc = $now,
                    status = CASE
                        WHEN ai_risk_approver_actor_id IS NOT NULL THEN 'Approved'
                        ELSE 'Pending'
                    END,
                    version = version + 1,
                    updated_at_utc = $now
                WHERE id = $id;
                """,
            DecisionKind.AiRiskApproval =>
                """
                UPDATE launch_requests
                SET ai_risk_approver_actor_id = $actorId,
                    ai_risk_approved_at_utc = $now,
                    status = CASE
                        WHEN product_approver_actor_id IS NOT NULL THEN 'Approved'
                        ELSE 'Pending'
                    END,
                    version = version + 1,
                    updated_at_utc = $now
                WHERE id = $id;
                """,
            DecisionKind.Rejection =>
                """
                UPDATE launch_requests
                SET status = 'Rejected',
                    rejector_actor_id = $actorId,
                    rejector_actor_role = $actorRole,
                    rejected_at_utc = $now,
                    version = version + 1,
                    updated_at_utc = $now
                WHERE id = $id;
                """,
            _ => throw new ArgumentOutOfRangeException(nameof(kind)),
        };

        await ExecuteAsync(
            connection,
            transaction,
            sql,
            cancellationToken,
            ("$actorId", actorId),
            ("$actorRole", actorRole),
            ("$now", occurredAt),
            ("$id", current.Id));
    }

    private static async Task<DecisionResult> RefuseAsync(
        SqliteConnection connection,
        SqliteTransaction transaction,
        LaunchRequestResource current,
        string action,
        string? actorId,
        string? actorRole,
        ProblemResource problem,
        CancellationToken cancellationToken)
    {
        await AppendAuditAsync(
            connection,
            transaction,
            current.Id,
            UtcNow(),
            action,
            actorId,
            actorRole,
            "Refused",
            problem.Code,
            current.Status,
            current.Version,
            cancellationToken);
        transaction.Commit();
        return new(null, problem);
    }

    private static async Task AppendAuditAsync(
        SqliteConnection connection,
        SqliteTransaction transaction,
        string requestId,
        string occurredAt,
        string action,
        string? actorId,
        string? actorRole,
        string outcome,
        string reasonCode,
        string statusAfter,
        int versionAfter,
        CancellationToken cancellationToken)
    {
        await ExecuteAsync(
            connection,
            transaction,
            """
            INSERT INTO audit_events (
                request_id, sequence, occurred_at_utc, action, actor_id, actor_role,
                outcome, reason_code, status_after, version_after)
            SELECT $requestId, COALESCE(MAX(sequence), 0) + 1, $occurredAt, $action,
                   $actorId, $actorRole, $outcome, $reasonCode, $statusAfter, $versionAfter
            FROM audit_events
            WHERE request_id = $requestId;
            """,
            cancellationToken,
            ("$requestId", requestId),
            ("$occurredAt", occurredAt),
            ("$action", action),
            ("$actorId", actorId),
            ("$actorRole", actorRole),
            ("$outcome", outcome),
            ("$reasonCode", reasonCode),
            ("$statusAfter", statusAfter),
            ("$versionAfter", versionAfter));
    }

    private static async Task<LaunchRequestResource> LoadRequiredAsync(
        SqliteConnection connection,
        SqliteTransaction transaction,
        string requestId,
        CancellationToken cancellationToken) =>
        await LoadAsync(connection, transaction, requestId, cancellationToken)
        ?? throw new DataException($"Launch request {requestId} disappeared inside its transaction.");

    private static async Task<LaunchRequestResource?> LoadAsync(
        SqliteConnection connection,
        SqliteTransaction transaction,
        string requestId,
        CancellationToken cancellationToken)
    {
        await using var command = CreateCommand(
            connection,
            transaction,
            """
            SELECT id, feature_name, status, requester_actor_id,
                   product_approver_actor_id, product_approved_at_utc,
                   ai_risk_approver_actor_id, ai_risk_approved_at_utc,
                   rejector_actor_id, rejector_actor_role, rejected_at_utc,
                   version, created_at_utc, updated_at_utc
            FROM launch_requests
            WHERE id = $id;
            """,
            ("$id", requestId));
        await using var reader = await command.ExecuteReaderAsync(cancellationToken);
        if (!await reader.ReadAsync(cancellationToken))
        {
            return null;
        }

        return new LaunchRequestResource(
            reader.GetString(0),
            reader.GetString(1),
            reader.GetString(2),
            reader.GetString(3),
            new ApprovalsResource(
                reader.IsDBNull(4)
                    ? null
                    : new ApprovalResource(reader.GetString(4), reader.GetString(5)),
                reader.IsDBNull(6)
                    ? null
                    : new ApprovalResource(reader.GetString(6), reader.GetString(7))),
            reader.IsDBNull(8)
                ? null
                : new RejectionResource(
                    reader.GetString(8),
                    reader.GetString(9),
                    reader.GetString(10)),
            reader.GetInt32(11),
            reader.GetString(12),
            reader.GetString(13));
    }

    private static async Task<HashSet<string>> ReadSchemaObjectsAsync(
        SqliteConnection connection,
        SqliteTransaction transaction,
        CancellationToken cancellationToken)
    {
        await using var command = CreateCommand(
            connection,
            transaction,
            """
            SELECT type || ':' || name
            FROM sqlite_master
            WHERE type IN ('table', 'trigger')
              AND name NOT LIKE 'sqlite_%';
            """);
        var objects = new HashSet<string>(StringComparer.Ordinal);
        await using var reader = await command.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
        {
            objects.Add(reader.GetString(0));
        }

        return objects;
    }

    private static async Task<int> ExecuteAsync(
        SqliteConnection connection,
        SqliteTransaction? transaction,
        string sql,
        CancellationToken cancellationToken,
        params (string Name, object? Value)[] parameters)
    {
        await using var command = CreateCommand(connection, transaction, sql, parameters);
        return await command.ExecuteNonQueryAsync(cancellationToken);
    }

    private static async Task<object?> ScalarAsync(
        SqliteConnection connection,
        SqliteTransaction transaction,
        string sql,
        CancellationToken cancellationToken)
    {
        await using var command = CreateCommand(connection, transaction, sql);
        return await command.ExecuteScalarAsync(cancellationToken);
    }

    private static SqliteCommand CreateCommand(
        SqliteConnection connection,
        SqliteTransaction? transaction,
        string sql,
        params (string Name, object? Value)[] parameters)
    {
        var command = connection.CreateCommand();
        command.CommandText = sql;
        command.Transaction = transaction;
        foreach (var (name, value) in parameters)
        {
            command.Parameters.AddWithValue(name, value ?? DBNull.Value);
        }

        return command;
    }

    private static bool RoleAuthorizes(ReferenceRole role, DecisionKind kind) =>
        kind switch
        {
            DecisionKind.ProductApproval => role == ReferenceRole.Product,
            DecisionKind.AiRiskApproval => role == ReferenceRole.AiRisk,
            DecisionKind.Rejection => role is ReferenceRole.Product or ReferenceRole.AiRisk,
            _ => false,
        };

    private static string ActionName(DecisionKind kind) =>
        kind switch
        {
            DecisionKind.ProductApproval => "ProductApproval",
            DecisionKind.AiRiskApproval => "AiRiskApproval",
            DecisionKind.Rejection => "Rejection",
            _ => throw new ArgumentOutOfRangeException(nameof(kind)),
        };

    private static string? RoleName(ReferenceRole? role) =>
        role switch
        {
            ReferenceRole.Requester => "Requester",
            ReferenceRole.Product => "Product",
            ReferenceRole.AiRisk => "AI-Risk",
            null => null,
            _ => throw new ArgumentOutOfRangeException(nameof(role)),
        };

    private static ProblemResource WithRequest(ProblemResource problem, string requestId) =>
        problem with { RequestId = requestId };

    private static string UtcNow() =>
        DateTimeOffset.UtcNow.ToString(
            "yyyy-MM-dd'T'HH:mm:ss.fffffff'Z'",
            CultureInfo.InvariantCulture);

    private const string SchemaSql =
        """
        CREATE TABLE launch_requests (
            id TEXT PRIMARY KEY
                CHECK (length(id) = 36 AND id = lower(id)),
            feature_name TEXT NOT NULL
                CHECK (
                    length(feature_name) BETWEEN 1 AND 120
                    AND feature_name = trim(feature_name)),
            status TEXT NOT NULL
                CHECK (status IN ('Pending', 'Approved', 'Rejected')),
            requester_actor_id TEXT NOT NULL
                CHECK (length(requester_actor_id) BETWEEN 1 AND 128),
            product_approver_actor_id TEXT,
            product_approved_at_utc TEXT,
            ai_risk_approver_actor_id TEXT,
            ai_risk_approved_at_utc TEXT,
            rejector_actor_id TEXT,
            rejector_actor_role TEXT
                CHECK (rejector_actor_role IS NULL OR rejector_actor_role IN ('Product', 'AI-Risk')),
            rejected_at_utc TEXT,
            version INTEGER NOT NULL CHECK (version >= 0),
            created_at_utc TEXT NOT NULL,
            updated_at_utc TEXT NOT NULL,
            CHECK ((product_approver_actor_id IS NULL) = (product_approved_at_utc IS NULL)),
            CHECK ((ai_risk_approver_actor_id IS NULL) = (ai_risk_approved_at_utc IS NULL)),
            CHECK (
                (rejector_actor_id IS NULL
                    AND rejector_actor_role IS NULL
                    AND rejected_at_utc IS NULL)
                OR
                (rejector_actor_id IS NOT NULL
                    AND rejector_actor_role IS NOT NULL
                    AND rejected_at_utc IS NOT NULL)),
            CHECK (
                product_approver_actor_id IS NULL
                OR product_approver_actor_id <> requester_actor_id),
            CHECK (
                ai_risk_approver_actor_id IS NULL
                OR ai_risk_approver_actor_id <> requester_actor_id),
            CHECK (
                product_approver_actor_id IS NULL
                OR ai_risk_approver_actor_id IS NULL
                OR product_approver_actor_id <> ai_risk_approver_actor_id),
            CHECK (
                (status = 'Pending'
                    AND rejector_actor_id IS NULL
                    AND NOT (
                        product_approver_actor_id IS NOT NULL
                        AND ai_risk_approver_actor_id IS NOT NULL))
                OR
                (status = 'Approved'
                    AND product_approver_actor_id IS NOT NULL
                    AND ai_risk_approver_actor_id IS NOT NULL
                    AND rejector_actor_id IS NULL)
                OR
                (status = 'Rejected'
                    AND rejector_actor_id IS NOT NULL
                    AND NOT (
                        product_approver_actor_id IS NOT NULL
                        AND ai_risk_approver_actor_id IS NOT NULL))),
            CHECK (
                version =
                    (product_approver_actor_id IS NOT NULL)
                    + (ai_risk_approver_actor_id IS NOT NULL)
                    + (rejector_actor_id IS NOT NULL))
        ) STRICT;

        CREATE TABLE audit_events (
            request_id TEXT NOT NULL,
            sequence INTEGER NOT NULL CHECK (sequence > 0),
            occurred_at_utc TEXT NOT NULL,
            action TEXT NOT NULL
                CHECK (action IN ('Submit', 'ProductApproval', 'AiRiskApproval', 'Rejection')),
            actor_id TEXT,
            actor_role TEXT
                CHECK (actor_role IS NULL OR actor_role IN ('Requester', 'Product', 'AI-Risk')),
            outcome TEXT NOT NULL CHECK (outcome IN ('Succeeded', 'Refused')),
            reason_code TEXT NOT NULL,
            status_after TEXT NOT NULL
                CHECK (status_after IN ('Pending', 'Approved', 'Rejected')),
            version_after INTEGER NOT NULL CHECK (version_after >= 0),
            PRIMARY KEY (request_id, sequence),
            FOREIGN KEY (request_id) REFERENCES launch_requests(id) ON DELETE RESTRICT,
            CHECK (
                (outcome = 'Succeeded'
                    AND reason_code IN (
                        'request_created', 'approval_recorded', 'request_rejected'))
                OR
                (outcome = 'Refused'
                    AND reason_code IN (
                        'identity_missing', 'identity_invalid', 'role_missing',
                        'role_unknown', 'role_mismatch', 'request_terminal',
                        'approval_already_recorded', 'requester_cannot_approve',
                        'approvers_not_distinct')))
        ) STRICT;

        CREATE TRIGGER launch_requests_no_delete
        BEFORE DELETE ON launch_requests
        BEGIN
            SELECT RAISE(ABORT, 'launch requests cannot be deleted');
        END;

        CREATE TRIGGER launch_requests_no_terminal_update
        BEFORE UPDATE ON launch_requests
        WHEN OLD.status IN ('Approved', 'Rejected')
        BEGIN
            SELECT RAISE(ABORT, 'terminal launch requests cannot be updated');
        END;

        CREATE TRIGGER audit_events_sequence_and_snapshot
        BEFORE INSERT ON audit_events
        BEGIN
            SELECT CASE
                WHEN NEW.sequence <> (
                    SELECT COALESCE(MAX(sequence), 0) + 1
                    FROM audit_events
                    WHERE request_id = NEW.request_id)
                THEN RAISE(ABORT, 'audit sequence must be contiguous')
            END;
            SELECT CASE
                WHEN NOT EXISTS (
                    SELECT 1
                    FROM launch_requests
                    WHERE id = NEW.request_id
                      AND status = NEW.status_after
                      AND version = NEW.version_after)
                THEN RAISE(ABORT, 'audit snapshot must match request state')
            END;
        END;

        CREATE TRIGGER audit_events_no_update
        BEFORE UPDATE ON audit_events
        BEGIN
            SELECT RAISE(ABORT, 'audit events are append-only');
        END;

        CREATE TRIGGER audit_events_no_delete
        BEFORE DELETE ON audit_events
        BEGIN
            SELECT RAISE(ABORT, 'audit events are append-only');
        END;
        """;
}
