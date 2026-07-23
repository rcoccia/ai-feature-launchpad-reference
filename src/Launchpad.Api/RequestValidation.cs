using System.Text.Json;
using Microsoft.Extensions.Primitives;

namespace Launchpad.Api;

internal static class RequestValidation
{
    internal static async Task<CreationBody> ReadCreationAsync(
        HttpRequest request,
        CancellationToken cancellationToken)
    {
        if (!request.HasJsonContentType())
        {
            return CreationBody.Invalid;
        }

        try
        {
            using var document = await JsonDocument.ParseAsync(
                request.Body,
                cancellationToken: cancellationToken);
            if (document.RootElement.ValueKind != JsonValueKind.Object)
            {
                return CreationBody.Invalid;
            }

            var properties = document.RootElement.EnumerateObject().ToArray();
            if (properties.Length != 1
                || properties[0].Name != "featureName"
                || properties[0].Value.ValueKind != JsonValueKind.String)
            {
                return CreationBody.Invalid;
            }

            var featureName = properties[0].Value.GetString()!.Trim();
            return featureName.Length is >= 1 and <= 120
                ? new CreationBody(featureName, null)
                : CreationBody.Invalid;
        }
        catch (JsonException)
        {
            return CreationBody.Invalid;
        }
    }

    internal static async Task<bool> HasBodyAsync(
        HttpRequest request,
        CancellationToken cancellationToken)
    {
        if (request.ContentLength is > 0 || request.Headers.ContainsKey("Transfer-Encoding"))
        {
            return true;
        }

        var buffer = new byte[1];
        return await request.Body.ReadAsync(buffer, cancellationToken) > 0;
    }

    internal static bool TryCanonicalGuid(string value, out string canonical)
    {
        canonical = string.Empty;
        if (!Guid.TryParseExact(value, "D", out var parsed))
        {
            return false;
        }

        canonical = parsed.ToString("D");
        return value == canonical;
    }
}

internal sealed record CreationBody(string? FeatureName, ProblemResource? Problem)
{
    internal static CreationBody Invalid { get; } =
        new(null, ApiContract.InvalidRequestBody());
}

internal enum ReferenceRole
{
    Requester,
    Product,
    AiRisk,
}

internal sealed record ReferenceIdentity(
    string? ActorId,
    ReferenceRole? Role,
    ProblemResource? ActorProblem,
    ProblemResource? RoleProblem)
{
    private const string ActorHeader = "X-Reference-Actor-Id";
    private const string RoleHeader = "X-Reference-Actor-Role";

    internal static ReferenceIdentity Parse(IHeaderDictionary headers)
    {
        var actor = ParseActor(headers);
        var role = ParseRole(headers);
        return new(actor.Value, role.Value, actor.Problem, role.Problem);
    }

    private static ParsedActor ParseActor(IHeaderDictionary headers)
    {
        if (!headers.TryGetValue(ActorHeader, out var values) || values.Count == 0)
        {
            return new(null, ApiContract.ActorMissing());
        }

        if (values.Count != 1)
        {
            return new(null, ApiContract.ActorInvalid());
        }

        var value = values[0] ?? string.Empty;
        if (value.Length is < 1 or > 128
            || value != value.Trim()
            || value.Contains(',', StringComparison.Ordinal)
            || value.Any(char.IsControl))
        {
            return new(null, ApiContract.ActorInvalid());
        }

        return new(value, null);
    }

    private static ParsedRole ParseRole(IHeaderDictionary headers)
    {
        if (!headers.TryGetValue(RoleHeader, out StringValues values) || values.Count == 0)
        {
            return new(null, ApiContract.RoleMissing());
        }

        if (values.Count != 1)
        {
            return new(null, ApiContract.RoleUnknown());
        }

        return values[0] switch
        {
            "Requester" => new(ReferenceRole.Requester, null),
            "Product" => new(ReferenceRole.Product, null),
            "AI-Risk" => new(ReferenceRole.AiRisk, null),
            _ => new(null, ApiContract.RoleUnknown()),
        };
    }

    private sealed record ParsedActor(string? Value, ProblemResource? Problem);

    private sealed record ParsedRole(ReferenceRole? Value, ProblemResource? Problem);
}
