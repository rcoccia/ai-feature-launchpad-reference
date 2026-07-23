using System.Net;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using Launchpad.Api;
using Microsoft.Data.Sqlite;

namespace Launchpad.Api.IntegrationTests;

public sealed class LaunchpadApiTests
{
    private const string WarningHeader = "X-Reference-Authentication-Warning";
    private const string WarningValue =
        "NON-PRODUCTION; caller-supplied headers are not authentication";

    public static TheoryData<string?, string?> InvalidCreationBodies =>
        new()
        {
            { null, null },
            { "{}", "application/json" },
            { """{"featureName":"Assistant","summary":"extra"}""", "application/json" },
            { """{"featureName":42}""", "application/json" },
            { """{"featureName":"   "}""", "application/json" },
            { $$"""{"featureName":"{{new string('x', 121)}}"}""", "application/json" },
            { """{"featureName":""", "application/json" },
            { """{"featureName":"Assistant"}""", "text/plain" },
        };

    [Fact]
    public async Task Creation_returns_exact_pending_resource_and_audit_contract()
    {
        using var scope = new TestScope();
        using var response = await SendAsync(
            scope.Client,
            CreationRequest("  Customer support answer assistant  "));

        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        Assert.NotNull(response.Headers.Location);
        using var document = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        Assert.Equal(
            [
                "id",
                "featureName",
                "status",
                "requesterActorId",
                "approvals",
                "rejection",
                "version",
                "createdAtUtc",
                "updatedAtUtc",
            ],
            document.RootElement.EnumerateObject().Select(property => property.Name));

        var resource = document.RootElement.Deserialize<LaunchRequestResource>(JsonOptions());
        Assert.NotNull(resource);
        Assert.Equal("Customer support answer assistant", resource.FeatureName);
        Assert.Equal("Pending", resource.Status);
        Assert.Equal("requester-1", resource.RequesterActorId);
        Assert.Null(resource.Approvals.Product);
        Assert.Null(resource.Approvals.AiRisk);
        Assert.Null(resource.Rejection);
        Assert.Equal(0, resource.Version);
        Assert.Equal($"/api/launch-requests/{resource.Id}", response.Headers.Location!.ToString());

        var audit = await GetAuditAsync(scope, resource.Id);
        Assert.Equal(resource.Id, audit.RequestId);
        Assert.Equal(resource.FeatureName, audit.FeatureName);
        var created = Assert.Single(audit.Events);
        Assert.Equal(1, created.Sequence);
        Assert.Equal("Submit", created.Action);
        Assert.Equal("requester-1", created.ActorId);
        Assert.Equal("Requester", created.ActorRole);
        Assert.Equal("Succeeded", created.Outcome);
        Assert.Equal("request_created", created.ReasonCode);
        Assert.Equal("Pending", created.StatusAfter);
        Assert.Equal(0, created.VersionAfter);
    }

    [Theory]
    [MemberData(nameof(InvalidCreationBodies))]
    public async Task Invalid_creation_shape_is_400_and_creates_no_request(
        string? body,
        string? contentType)
    {
        using var scope = new TestScope();
        using var request = new HttpRequestMessage(HttpMethod.Post, "/api/launch-requests");
        AddIdentity(request, "requester-1", "Requester");
        if (body is not null)
        {
            request.Content = new StringContent(body, Encoding.UTF8, contentType!);
        }

        using var response = await SendAsync(scope.Client, request);
        await AssertProblemAsync(
            response,
            HttpStatusCode.BadRequest,
            "invalid_request_body",
            requestId: null);
        Assert.Equal(0L, await ScalarAsync(scope.DatabasePath, "SELECT COUNT(*) FROM launch_requests;"));
        Assert.Equal(0L, await ScalarAsync(scope.DatabasePath, "SELECT COUNT(*) FROM audit_events;"));
    }

    [Fact]
    public async Task Creation_identity_and_role_fail_closed_without_a_request()
    {
        using var scope = new TestScope();

        using var missingActor = CreationRequest("Assistant", actor: null, role: "Requester");
        using var missingActorResponse = await SendAsync(scope.Client, missingActor);
        await AssertProblemAsync(
            missingActorResponse,
            HttpStatusCode.Unauthorized,
            "identity_missing",
            requestId: null);

        using var unknownRole = CreationRequest("Assistant", role: "Risk");
        using var unknownRoleResponse = await SendAsync(scope.Client, unknownRole);
        await AssertProblemAsync(
            unknownRoleResponse,
            HttpStatusCode.Forbidden,
            "role_unknown",
            requestId: null);

        using var mismatchedRole = CreationRequest("Assistant", role: "Product");
        using var mismatchedRoleResponse = await SendAsync(scope.Client, mismatchedRole);
        await AssertProblemAsync(
            mismatchedRoleResponse,
            HttpStatusCode.Forbidden,
            "role_mismatch",
            requestId: null);

        Assert.Equal(0L, await ScalarAsync(scope.DatabasePath, "SELECT COUNT(*) FROM launch_requests;"));
    }

    [Theory]
    [InlineData("product", "Product", "product-approver", "ai-risk", "AI-Risk", "risk-approver")]
    [InlineData("ai-risk", "AI-Risk", "risk-approver", "product", "Product", "product-approver")]
    public async Task Distinct_approvals_reach_approved_in_either_order(
        string firstPath,
        string firstRole,
        string firstActor,
        string secondPath,
        string secondRole,
        string secondActor)
    {
        using var scope = new TestScope();
        var created = await CreateAsync(scope);

        using var first = await SendAsync(
            scope.Client,
            DecisionRequest(created.Id, $"approvals/{firstPath}", firstActor, firstRole));
        Assert.Equal(HttpStatusCode.OK, first.StatusCode);
        var pending = await first.Content.ReadFromJsonAsync<LaunchRequestResource>();
        Assert.NotNull(pending);
        Assert.Equal("Pending", pending.Status);
        Assert.Equal(1, pending.Version);

        using var second = await SendAsync(
            scope.Client,
            DecisionRequest(created.Id, $"approvals/{secondPath}", secondActor, secondRole));
        Assert.Equal(HttpStatusCode.OK, second.StatusCode);
        var approved = await second.Content.ReadFromJsonAsync<LaunchRequestResource>();
        Assert.NotNull(approved);
        Assert.Equal("Approved", approved.Status);
        Assert.Equal(2, approved.Version);
        Assert.Equal("product-approver", approved.Approvals.Product!.ActorId);
        Assert.Equal("risk-approver", approved.Approvals.AiRisk!.ActorId);

        var audit = await GetAuditAsync(scope, created.Id);
        Assert.Equal([1, 2, 3], audit.Events.Select(entry => entry.Sequence));
        Assert.All(audit.Events, entry => Assert.Equal("Succeeded", entry.Outcome));
        Assert.Equal("Approved", audit.Events[^1].StatusAfter);
        Assert.Equal(2, audit.Events[^1].VersionAfter);
    }

    [Fact]
    public async Task Requester_and_cross_role_actor_separation_refusals_are_audited()
    {
        using var scope = new TestScope();
        var created = await CreateAsync(scope);

        using var requesterApproval = await SendAsync(
            scope.Client,
            DecisionRequest(created.Id, "approvals/product", "requester-1", "Product"));
        await AssertProblemAsync(
            requesterApproval,
            HttpStatusCode.Conflict,
            "requester_cannot_approve",
            created.Id);

        using var productApproval = await SendAsync(
            scope.Client,
            DecisionRequest(created.Id, "approvals/product", "shared-approver", "Product"));
        Assert.Equal(HttpStatusCode.OK, productApproval.StatusCode);

        using var riskApproval = await SendAsync(
            scope.Client,
            DecisionRequest(created.Id, "approvals/ai-risk", "shared-approver", "AI-Risk"));
        await AssertProblemAsync(
            riskApproval,
            HttpStatusCode.Conflict,
            "approvers_not_distinct",
            created.Id);

        var resource = await GetAsync(scope, created.Id);
        Assert.Equal("Pending", resource.Status);
        Assert.Equal(1, resource.Version);

        var audit = await GetAuditAsync(scope, created.Id);
        Assert.Equal(
            ["request_created", "requester_cannot_approve", "approval_recorded", "approvers_not_distinct"],
            audit.Events.Select(entry => entry.ReasonCode));
        Assert.Equal([0, 0, 1, 1], audit.Events.Select(entry => entry.VersionAfter));
    }

    [Fact]
    public async Task Duplicate_approval_is_audited_without_changing_state()
    {
        using var scope = new TestScope();
        var created = await CreateAsync(scope);

        using var success = await SendAsync(
            scope.Client,
            DecisionRequest(created.Id, "approvals/product", "product-1", "Product"));
        Assert.Equal(HttpStatusCode.OK, success.StatusCode);

        using var duplicate = await SendAsync(
            scope.Client,
            DecisionRequest(created.Id, "approvals/product", "product-2", "Product"));
        await AssertProblemAsync(
            duplicate,
            HttpStatusCode.Conflict,
            "approval_already_recorded",
            created.Id);

        var resource = await GetAsync(scope, created.Id);
        Assert.Equal("Pending", resource.Status);
        Assert.Equal(1, resource.Version);
        Assert.Equal("product-1", resource.Approvals.Product!.ActorId);

        var audit = await GetAuditAsync(scope, created.Id);
        Assert.Equal(["Succeeded", "Succeeded", "Refused"], audit.Events.Select(entry => entry.Outcome));
        Assert.Equal("approval_already_recorded", audit.Events[^1].ReasonCode);
        Assert.Equal(1, audit.Events[^1].VersionAfter);
    }

    [Theory]
    [InlineData("Product")]
    [InlineData("AI-Risk")]
    public async Task Either_authorized_role_can_reject_and_retain_prior_approval(string rejectingRole)
    {
        using var scope = new TestScope();
        var created = await CreateAsync(scope);
        using var approval = await SendAsync(
            scope.Client,
            DecisionRequest(created.Id, "approvals/product", "product-1", "Product"));
        Assert.Equal(HttpStatusCode.OK, approval.StatusCode);

        using var rejection = await SendAsync(
            scope.Client,
            DecisionRequest(created.Id, "rejection", "requester-1", rejectingRole));
        Assert.Equal(HttpStatusCode.OK, rejection.StatusCode);
        var rejected = await rejection.Content.ReadFromJsonAsync<LaunchRequestResource>();
        Assert.NotNull(rejected);
        Assert.Equal("Rejected", rejected.Status);
        Assert.Equal(2, rejected.Version);
        Assert.Equal("product-1", rejected.Approvals.Product!.ActorId);
        Assert.Equal("requester-1", rejected.Rejection!.ActorId);
        Assert.Equal(rejectingRole, rejected.Rejection.ActorRole);
    }

    [Fact]
    public async Task Approved_and_rejected_requests_are_terminal_and_refusals_are_audited()
    {
        using var scope = new TestScope();
        var approved = await CreateAsync(scope, "Approved feature");
        await ApproveAsync(scope, approved.Id);
        var approvedBefore = await GetAsync(scope, approved.Id);
        var approvedAuditBefore = await GetAuditAsync(scope, approved.Id);

        using var approvedRejection = await SendAsync(
            scope.Client,
            DecisionRequest(approved.Id, "rejection", "product-2", "Product"));
        await AssertProblemAsync(
            approvedRejection,
            HttpStatusCode.Conflict,
            "request_terminal",
            approved.Id);
        var approvedAfter = await GetAsync(scope, approved.Id);
        var approvedAuditAfter = await GetAuditAsync(scope, approved.Id);
        Assert.Equal(approvedBefore.Status, approvedAfter.Status);
        Assert.Equal(approvedBefore.Version, approvedAfter.Version);
        Assert.Equal(approvedAuditBefore.Events.Count + 1, approvedAuditAfter.Events.Count);
        Assert.Equal(
            Enumerable.Range(1, approvedAuditAfter.Events.Count),
            approvedAuditAfter.Events.Select(entry => entry.Sequence));
        var approvedRefusal = approvedAuditAfter.Events[^1];
        Assert.Equal("Refused", approvedRefusal.Outcome);
        Assert.Equal("request_terminal", approvedRefusal.ReasonCode);
        Assert.Equal(approvedBefore.Status, approvedRefusal.StatusAfter);
        Assert.Equal(approvedBefore.Version, approvedRefusal.VersionAfter);

        var rejected = await CreateAsync(scope, "Rejected feature");
        using var rejection = await SendAsync(
            scope.Client,
            DecisionRequest(rejected.Id, "rejection", "risk-1", "AI-Risk"));
        Assert.Equal(HttpStatusCode.OK, rejection.StatusCode);
        var rejectedBefore = await GetAsync(scope, rejected.Id);
        var rejectedAuditBefore = await GetAuditAsync(scope, rejected.Id);

        using var repeatedRejection = await SendAsync(
            scope.Client,
            DecisionRequest(rejected.Id, "rejection", "product-1", "Product"));
        await AssertProblemAsync(
            repeatedRejection,
            HttpStatusCode.Conflict,
            "request_terminal",
            rejected.Id);
        var rejectedAfter = await GetAsync(scope, rejected.Id);
        var rejectedAuditAfter = await GetAuditAsync(scope, rejected.Id);
        Assert.Equal(rejectedBefore.Status, rejectedAfter.Status);
        Assert.Equal(rejectedBefore.Version, rejectedAfter.Version);
        Assert.Equal(rejectedAuditBefore.Events.Count + 1, rejectedAuditAfter.Events.Count);
        Assert.Equal(
            Enumerable.Range(1, rejectedAuditAfter.Events.Count),
            rejectedAuditAfter.Events.Select(entry => entry.Sequence));
        var rejectedRefusal = rejectedAuditAfter.Events[^1];
        Assert.Equal("Refused", rejectedRefusal.Outcome);
        Assert.Equal("request_terminal", rejectedRefusal.ReasonCode);
        Assert.Equal(rejectedBefore.Status, rejectedRefusal.StatusAfter);
        Assert.Equal(rejectedBefore.Version, rejectedRefusal.VersionAfter);
    }

    [Fact]
    public async Task Existing_target_identity_and_role_refusals_are_ordered_and_audited()
    {
        using var scope = new TestScope();
        var created = await CreateAsync(scope);

        using var missingActor = await SendAsync(
            scope.Client,
            DecisionRequest(created.Id, "approvals/product", null, "Product"));
        await AssertProblemAsync(
            missingActor,
            HttpStatusCode.Unauthorized,
            "identity_missing",
            created.Id);

        using var invalidActor = await SendAsync(
            scope.Client,
            DecisionRequest(created.Id, "approvals/product", " bad ", "Product"));
        await AssertProblemAsync(
            invalidActor,
            HttpStatusCode.Unauthorized,
            "identity_invalid",
            created.Id);

        using var missingRole = await SendAsync(
            scope.Client,
            DecisionRequest(created.Id, "approvals/product", "product-1", null));
        await AssertProblemAsync(
            missingRole,
            HttpStatusCode.Forbidden,
            "role_missing",
            created.Id);

        using var unknownRole = await SendAsync(
            scope.Client,
            DecisionRequest(created.Id, "approvals/product", "product-1", "Risk"));
        await AssertProblemAsync(
            unknownRole,
            HttpStatusCode.Forbidden,
            "role_unknown",
            created.Id);

        using var mismatchedRole = await SendAsync(
            scope.Client,
            DecisionRequest(created.Id, "approvals/product", "product-1", "AI-Risk"));
        await AssertProblemAsync(
            mismatchedRole,
            HttpStatusCode.Forbidden,
            "role_mismatch",
            created.Id);

        var audit = await GetAuditAsync(scope, created.Id);
        Assert.Equal(
            [
                "request_created",
                "identity_missing",
                "identity_invalid",
                "role_missing",
                "role_unknown",
                "role_mismatch",
            ],
            audit.Events.Select(entry => entry.ReasonCode));
        Assert.All(audit.Events.Skip(1), entry => Assert.Equal("Refused", entry.Outcome));
        Assert.All(audit.Events, entry => Assert.Equal(0, entry.VersionAfter));
    }

    [Fact]
    public async Task Transport_and_missing_target_failures_are_not_request_attached()
    {
        using var scope = new TestScope();
        var created = await CreateAsync(scope);

        using var decisionBody = DecisionRequest(
            created.Id,
            "approvals/product",
            "product-1",
            "Product");
        decisionBody.Content = JsonContent.Create(new { unexpected = true });
        using var decisionBodyResponse = await SendAsync(scope.Client, decisionBody);
        await AssertProblemAsync(
            decisionBodyResponse,
            HttpStatusCode.BadRequest,
            "body_not_allowed",
            requestId: null);

        using var malformedId = await SendAsync(
            scope.Client,
            DecisionRequest("NOT-A-GUID", "approvals/product", "product-1", "Product"));
        await AssertProblemAsync(
            malformedId,
            HttpStatusCode.BadRequest,
            "invalid_request_id",
            requestId: null);

        var absentId = Guid.NewGuid().ToString("D");
        using var absent = await SendAsync(
            scope.Client,
            DecisionRequest(absentId, "approvals/product", null, null));
        await AssertProblemAsync(
            absent,
            HttpStatusCode.NotFound,
            "request_not_found",
            requestId: null);

        Assert.Single((await GetAuditAsync(scope, created.Id)).Events);
        Assert.Equal(1L, await ScalarAsync(scope.DatabasePath, "SELECT COUNT(*) FROM audit_events;"));
    }

    [Fact]
    public async Task Read_routes_require_no_identity_and_return_warned_404s()
    {
        using var scope = new TestScope();
        var created = await CreateAsync(scope);

        using var get = await SendAsync(
            scope.Client,
            new HttpRequestMessage(HttpMethod.Get, $"/api/launch-requests/{created.Id}"));
        Assert.Equal(HttpStatusCode.OK, get.StatusCode);

        using var audit = await SendAsync(
            scope.Client,
            new HttpRequestMessage(HttpMethod.Get, $"/api/launch-requests/{created.Id}/audit"));
        Assert.Equal(HttpStatusCode.OK, audit.StatusCode);

        using var absent = await SendAsync(
            scope.Client,
            new HttpRequestMessage(
                HttpMethod.Get,
                $"/api/launch-requests/{Guid.NewGuid():D}"));
        await AssertProblemAsync(
            absent,
            HttpStatusCode.NotFound,
            "request_not_found",
            requestId: null);
    }

    [Fact]
    public async Task File_backed_state_and_audit_survive_host_reload()
    {
        using var directory = new TemporaryDirectory();
        LaunchRequestResource created;
        AuditResource before;
        using (var firstFactory = new LaunchpadFactory(directory.DatabasePath))
        using (var firstClient = firstFactory.CreateClient())
        {
            created = await CreateAsync(firstClient, "Reload feature");
            using var approval = await SendAsync(
                firstClient,
                DecisionRequest(created.Id, "approvals/product", "product-1", "Product"));
            Assert.Equal(HttpStatusCode.OK, approval.StatusCode);
            before = await GetAuditAsync(firstClient, created.Id);
        }

        SqliteConnection.ClearAllPools();
        using var secondFactory = new LaunchpadFactory(directory.DatabasePath);
        using var secondClient = secondFactory.CreateClient();
        var afterResource = await GetAsync(secondClient, created.Id);
        var afterAudit = await GetAuditAsync(secondClient, created.Id);
        Assert.Equal("Pending", afterResource.Status);
        Assert.Equal(1, afterResource.Version);
        Assert.Equal("product-1", afterResource.Approvals.Product!.ActorId);
        Assert.Equal(before.RequestId, afterAudit.RequestId);
        Assert.Equal(before.FeatureName, afterAudit.FeatureName);
        Assert.Equal(before.Events, afterAudit.Events);
    }

    [Fact]
    public async Task Parallel_distinct_approvals_serialize_to_approved()
    {
        using var scope = new TestScope();
        var created = await CreateAsync(scope);

        var responses = await Task.WhenAll(
            SendAsync(
                scope.Client,
                DecisionRequest(created.Id, "approvals/product", "product-1", "Product")),
            SendAsync(
                scope.Client,
                DecisionRequest(created.Id, "approvals/ai-risk", "risk-1", "AI-Risk")));
        using var first = responses[0];
        using var second = responses[1];
        Assert.All(responses, response => Assert.Equal(HttpStatusCode.OK, response.StatusCode));

        var resource = await GetAsync(scope, created.Id);
        Assert.Equal("Approved", resource.Status);
        Assert.Equal(2, resource.Version);
        var audit = await GetAuditAsync(scope, created.Id);
        Assert.Equal([1, 2, 3], audit.Events.Select(entry => entry.Sequence));
        Assert.Equal([0, 1, 2], audit.Events.Select(entry => entry.VersionAfter));
    }

    [Fact]
    public async Task Parallel_duplicate_approval_has_one_success_and_one_audited_conflict()
    {
        using var scope = new TestScope();
        var created = await CreateAsync(scope);

        var responses = await Task.WhenAll(
            SendAsync(
                scope.Client,
                DecisionRequest(created.Id, "approvals/product", "product-1", "Product")),
            SendAsync(
                scope.Client,
                DecisionRequest(created.Id, "approvals/product", "product-2", "Product")));
        using var first = responses[0];
        using var second = responses[1];
        Assert.Equal(
            [HttpStatusCode.OK, HttpStatusCode.Conflict],
            responses.Select(response => response.StatusCode).Order());

        var audit = await GetAuditAsync(scope, created.Id);
        Assert.Equal(3, audit.Events.Count);
        Assert.Equal("approval_already_recorded", audit.Events[^1].ReasonCode);
        Assert.Equal("Refused", audit.Events[^1].Outcome);
        Assert.Equal(1, audit.Events[^1].VersionAfter);
    }

    [Fact]
    public async Task Parallel_same_actor_for_both_roles_has_one_audited_separation_conflict()
    {
        using var scope = new TestScope();
        var created = await CreateAsync(scope);

        var responses = await Task.WhenAll(
            SendAsync(
                scope.Client,
                DecisionRequest(created.Id, "approvals/product", "shared", "Product")),
            SendAsync(
                scope.Client,
                DecisionRequest(created.Id, "approvals/ai-risk", "shared", "AI-Risk")));
        using var first = responses[0];
        using var second = responses[1];
        Assert.Equal(
            [HttpStatusCode.OK, HttpStatusCode.Conflict],
            responses.Select(response => response.StatusCode).Order());

        var resource = await GetAsync(scope, created.Id);
        Assert.Equal("Pending", resource.Status);
        Assert.Equal(1, resource.Version);
        var audit = await GetAuditAsync(scope, created.Id);
        Assert.Equal("approvers_not_distinct", audit.Events[^1].ReasonCode);
        Assert.Equal([1, 2, 3], audit.Events.Select(entry => entry.Sequence));
    }

    [Fact]
    public async Task Rejection_race_is_consistent_with_serial_commit_order()
    {
        using var scope = new TestScope();
        var created = await CreateAsync(scope);

        var responses = await Task.WhenAll(
            SendAsync(
                scope.Client,
                DecisionRequest(created.Id, "approvals/product", "product-1", "Product")),
            SendAsync(
                scope.Client,
                DecisionRequest(created.Id, "rejection", "risk-1", "AI-Risk")));
        using var approval = responses[0];
        using var rejection = responses[1];
        Assert.Equal(HttpStatusCode.OK, rejection.StatusCode);
        Assert.True(
            approval.StatusCode is HttpStatusCode.OK or HttpStatusCode.Conflict,
            $"Unexpected approval status {approval.StatusCode}.");

        var resource = await GetAsync(scope, created.Id);
        var audit = await GetAuditAsync(scope, created.Id);
        Assert.Equal("Rejected", resource.Status);
        Assert.Equal(resource.Version, audit.Events[^1].VersionAfter);
        Assert.Equal(Enumerable.Range(1, audit.Events.Count), audit.Events.Select(entry => entry.Sequence));
        Assert.All(
            audit.Events,
            entry =>
            {
                Assert.Equal(resource.Id, audit.RequestId);
                Assert.True(entry.VersionAfter <= resource.Version);
            });
    }

    [Fact]
    public async Task SQLite_schema_and_triggers_enforce_append_only_durable_state()
    {
        using var scope = new TestScope();
        var created = await CreateAsync(scope);
        await ApproveAsync(scope, created.Id);

        Assert.Equal(1L, await ScalarAsync(scope.DatabasePath, "PRAGMA user_version;"));
        Assert.Equal(
            2L,
            await ScalarAsync(
                scope.DatabasePath,
                "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%';"));
        Assert.Equal(
            2L,
            await ScalarAsync(
                scope.DatabasePath,
                "SELECT COUNT(*) FROM sqlite_master WHERE type = 'index';"));

        await AssertSqliteAbortAsync(
            scope.DatabasePath,
            "UPDATE audit_events SET reason_code = 'request_created' WHERE request_id = $id;",
            created.Id,
            "append-only");
        await AssertSqliteAbortAsync(
            scope.DatabasePath,
            "DELETE FROM audit_events WHERE request_id = $id;",
            created.Id,
            "append-only");
        await AssertSqliteAbortAsync(
            scope.DatabasePath,
            "DELETE FROM launch_requests WHERE id = $id;",
            created.Id,
            "cannot be deleted");
        await AssertSqliteAbortAsync(
            scope.DatabasePath,
            "UPDATE launch_requests SET updated_at_utc = updated_at_utc WHERE id = $id;",
            created.Id,
            "terminal");
    }

    [Fact]
    public void Unknown_schema_version_stops_startup()
    {
        using var directory = new TemporaryDirectory();
        using (var connection = OpenConnection(directory.DatabasePath))
        {
            connection.Open();
            using var command = connection.CreateCommand();
            command.CommandText = "PRAGMA user_version=2;";
            command.ExecuteNonQuery();
        }

        using var factory = new LaunchpadFactory(directory.DatabasePath);
        var exception = Assert.Throws<InvalidOperationException>(() => factory.CreateClient());
        Assert.Contains("unsupported", exception.ToString(), StringComparison.OrdinalIgnoreCase);
    }

    [Fact]
    public void Production_environment_stops_before_serving()
    {
        using var directory = new TemporaryDirectory();
        using var factory = new LaunchpadFactory(directory.DatabasePath, "Production");
        var exception = Assert.Throws<InvalidOperationException>(() => factory.CreateClient());
        Assert.Contains(
            "Development or Testing",
            exception.ToString(),
            StringComparison.Ordinal);
    }

    private static async Task ApproveAsync(TestScope scope, string requestId)
    {
        using var product = await SendAsync(
            scope.Client,
            DecisionRequest(requestId, "approvals/product", "product-1", "Product"));
        Assert.Equal(HttpStatusCode.OK, product.StatusCode);
        using var risk = await SendAsync(
            scope.Client,
            DecisionRequest(requestId, "approvals/ai-risk", "risk-1", "AI-Risk"));
        Assert.Equal(HttpStatusCode.OK, risk.StatusCode);
    }

    private static async Task<LaunchRequestResource> CreateAsync(
        TestScope scope,
        string featureName = "Answer assistant") =>
        await CreateAsync(scope.Client, featureName);

    private static async Task<LaunchRequestResource> CreateAsync(
        HttpClient client,
        string featureName)
    {
        using var response = await SendAsync(client, CreationRequest(featureName));
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        return await response.Content.ReadFromJsonAsync<LaunchRequestResource>()
            ?? throw new JsonException("Creation response did not contain a launch request.");
    }

    private static async Task<LaunchRequestResource> GetAsync(TestScope scope, string requestId) =>
        await GetAsync(scope.Client, requestId);

    private static async Task<LaunchRequestResource> GetAsync(
        HttpClient client,
        string requestId)
    {
        using var response = await SendAsync(
            client,
            new HttpRequestMessage(HttpMethod.Get, $"/api/launch-requests/{requestId}"));
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        return await response.Content.ReadFromJsonAsync<LaunchRequestResource>()
            ?? throw new JsonException("GET response did not contain a launch request.");
    }

    private static async Task<AuditResource> GetAuditAsync(TestScope scope, string requestId) =>
        await GetAuditAsync(scope.Client, requestId);

    private static async Task<AuditResource> GetAuditAsync(
        HttpClient client,
        string requestId)
    {
        using var response = await SendAsync(
            client,
            new HttpRequestMessage(
                HttpMethod.Get,
                $"/api/launch-requests/{requestId}/audit"));
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        return await response.Content.ReadFromJsonAsync<AuditResource>()
            ?? throw new JsonException("Audit response did not contain an audit resource.");
    }

    private static HttpRequestMessage CreationRequest(
        string featureName,
        string? actor = "requester-1",
        string? role = "Requester")
    {
        var request = new HttpRequestMessage(HttpMethod.Post, "/api/launch-requests")
        {
            Content = JsonContent.Create(new { featureName }),
        };
        AddIdentity(request, actor, role);
        return request;
    }

    private static HttpRequestMessage DecisionRequest(
        string requestId,
        string command,
        string? actor,
        string? role)
    {
        var request = new HttpRequestMessage(
            HttpMethod.Post,
            $"/api/launch-requests/{requestId}/{command}");
        AddIdentity(request, actor, role);
        return request;
    }

    private static void AddIdentity(
        HttpRequestMessage request,
        string? actor,
        string? role)
    {
        if (actor is not null)
        {
            request.Headers.TryAddWithoutValidation("X-Reference-Actor-Id", actor);
        }

        if (role is not null)
        {
            request.Headers.TryAddWithoutValidation("X-Reference-Actor-Role", role);
        }
    }

    private static async Task<HttpResponseMessage> SendAsync(
        HttpClient client,
        HttpRequestMessage request)
    {
        var response = await client.SendAsync(request);
        Assert.True(response.Headers.TryGetValues(WarningHeader, out var values));
        Assert.Equal(WarningValue, Assert.Single(values));
        return response;
    }

    private static async Task AssertProblemAsync(
        HttpResponseMessage response,
        HttpStatusCode status,
        string code,
        string? requestId)
    {
        Assert.Equal(status, response.StatusCode);
        Assert.Equal("application/problem+json", response.Content.Headers.ContentType!.MediaType);
        var problem = await response.Content.ReadFromJsonAsync<ProblemResource>();
        Assert.NotNull(problem);
        Assert.Equal((int)status, problem.Status);
        Assert.Equal(code, problem.Code);
        Assert.Equal(requestId, problem.RequestId);

        using var document = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        Assert.Equal(
            requestId is null
                ? ["title", "status", "code"]
                : ["title", "status", "code", "requestId"],
            document.RootElement.EnumerateObject().Select(property => property.Name));
    }

    private static JsonSerializerOptions JsonOptions() =>
        new(JsonSerializerDefaults.Web);

    private static SqliteConnection OpenConnection(string databasePath) =>
        new(
            new SqliteConnectionStringBuilder
            {
                DataSource = databasePath,
                Mode = SqliteOpenMode.ReadWriteCreate,
                ForeignKeys = true,
                Pooling = false,
            }.ToString());

    private static async Task<long> ScalarAsync(string databasePath, string sql)
    {
        await using var connection = OpenConnection(databasePath);
        await connection.OpenAsync();
        await using var command = connection.CreateCommand();
        command.CommandText = sql;
        return Convert.ToInt64(await command.ExecuteScalarAsync());
    }

    private static async Task AssertSqliteAbortAsync(
        string databasePath,
        string sql,
        string requestId,
        string expectedMessage)
    {
        await using var connection = OpenConnection(databasePath);
        await connection.OpenAsync();
        await using var command = connection.CreateCommand();
        command.CommandText = sql;
        command.Parameters.AddWithValue("$id", requestId);
        var exception = await Assert.ThrowsAsync<SqliteException>(
            async () => await command.ExecuteNonQueryAsync());
        Assert.Contains(expectedMessage, exception.Message, StringComparison.OrdinalIgnoreCase);
    }

    private sealed class TestScope : IDisposable
    {
        private readonly TemporaryDirectory _directory = new();
        private readonly LaunchpadFactory _factory;

        internal TestScope()
        {
            _factory = new LaunchpadFactory(_directory.DatabasePath);
            Client = _factory.CreateClient(
                new Microsoft.AspNetCore.Mvc.Testing.WebApplicationFactoryClientOptions
                {
                    AllowAutoRedirect = false,
                });
        }

        internal string DatabasePath => _directory.DatabasePath;

        internal HttpClient Client { get; }

        public void Dispose()
        {
            Client.Dispose();
            _factory.Dispose();
            SqliteConnection.ClearAllPools();
            _directory.Dispose();
        }
    }

    private sealed class TemporaryDirectory : IDisposable
    {
        private readonly string _path =
            Path.Combine(Path.GetTempPath(), $"launchpad-{Guid.NewGuid():N}");

        internal TemporaryDirectory()
        {
            Directory.CreateDirectory(_path);
        }

        internal string DatabasePath => Path.Combine(_path, "launchpad.db");

        public void Dispose()
        {
            SqliteConnection.ClearAllPools();
            Directory.Delete(_path, recursive: true);
        }
    }
}
