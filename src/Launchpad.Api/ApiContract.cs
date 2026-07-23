using System.Text.Json.Serialization;

namespace Launchpad.Api;

internal static class ApiContract
{
    internal const string WarningHeaderName = "X-Reference-Authentication-Warning";
    internal const string WarningHeaderValue =
        "NON-PRODUCTION; caller-supplied headers are not authentication";

    internal static IResult Problem(ProblemResource problem) =>
        Results.Json(
            problem,
            statusCode: problem.Status,
            contentType: "application/problem+json");

    internal static ProblemResource InvalidRequestBody() =>
        new("Invalid request body", StatusCodes.Status400BadRequest, "invalid_request_body");

    internal static ProblemResource BodyNotAllowed() =>
        new("Request body is not allowed", StatusCodes.Status400BadRequest, "body_not_allowed");

    internal static ProblemResource InvalidRequestId() =>
        new("Request ID is invalid", StatusCodes.Status400BadRequest, "invalid_request_id");

    internal static ProblemResource RequestNotFound() =>
        new("Launch request was not found", StatusCodes.Status404NotFound, "request_not_found");

    internal static ProblemResource ActorMissing(string? requestId = null) =>
        new(
            "Reference actor is required",
            StatusCodes.Status401Unauthorized,
            "identity_missing",
            requestId);

    internal static ProblemResource ActorInvalid(string? requestId = null) =>
        new(
            "Reference actor is invalid",
            StatusCodes.Status401Unauthorized,
            "identity_invalid",
            requestId);

    internal static ProblemResource RoleMissing(string? requestId = null) =>
        new(
            "Reference actor role is required",
            StatusCodes.Status403Forbidden,
            "role_missing",
            requestId);

    internal static ProblemResource RoleUnknown(string? requestId = null) =>
        new(
            "Reference actor role is invalid",
            StatusCodes.Status403Forbidden,
            "role_unknown",
            requestId);

    internal static ProblemResource RoleMismatch(string? requestId = null) =>
        new(
            "Reference actor role is not authorized for this command",
            StatusCodes.Status403Forbidden,
            "role_mismatch",
            requestId);

    internal static ProblemResource RequestTerminal(string requestId) =>
        new(
            "Launch request is terminal",
            StatusCodes.Status409Conflict,
            "request_terminal",
            requestId);

    internal static ProblemResource ApprovalAlreadyRecorded(string requestId) =>
        new(
            "Approval is already recorded",
            StatusCodes.Status409Conflict,
            "approval_already_recorded",
            requestId);

    internal static ProblemResource RequesterCannotApprove(string requestId) =>
        new(
            "Requester cannot approve the launch request",
            StatusCodes.Status409Conflict,
            "requester_cannot_approve",
            requestId);

    internal static ProblemResource ApproversNotDistinct(string requestId) =>
        new(
            "Product and AI-Risk approvers must be distinct",
            StatusCodes.Status409Conflict,
            "approvers_not_distinct",
            requestId);

    internal static ProblemResource DatabaseUnavailable() =>
        new(
            "Launchpad database is unavailable",
            StatusCodes.Status503ServiceUnavailable,
            "database_unavailable");
}

public sealed record ProblemResource(
    string Title,
    int Status,
    string Code,
    [property: JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    string? RequestId = null);

public sealed record ApprovalResource(string ActorId, string RecordedAtUtc);

public sealed record RejectionResource(
    string ActorId,
    string ActorRole,
    string RecordedAtUtc);

public sealed record ApprovalsResource(
    ApprovalResource? Product,
    ApprovalResource? AiRisk);

public sealed record LaunchRequestResource(
    string Id,
    string FeatureName,
    string Status,
    string RequesterActorId,
    ApprovalsResource Approvals,
    RejectionResource? Rejection,
    int Version,
    string CreatedAtUtc,
    string UpdatedAtUtc);

public sealed record AuditEventResource(
    int Sequence,
    string OccurredAtUtc,
    string Action,
    string? ActorId,
    string? ActorRole,
    string Outcome,
    string ReasonCode,
    string StatusAfter,
    int VersionAfter);

public sealed record AuditResource(
    string RequestId,
    string FeatureName,
    IReadOnlyList<AuditEventResource> Events);

internal sealed record DecisionResult(
    LaunchRequestResource? Resource,
    ProblemResource? Problem);
