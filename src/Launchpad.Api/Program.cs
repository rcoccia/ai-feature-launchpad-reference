using Launchpad.Api;
using Microsoft.Data.Sqlite;

var builder = WebApplication.CreateBuilder(args);

if (!builder.Environment.IsDevelopment() && !builder.Environment.IsEnvironment("Testing"))
{
    throw new InvalidOperationException(
        "AI Feature Launchpad starts only in Development or Testing. "
        + "Its trusted headers are not production authentication.");
}

builder.Services.AddSingleton(serviceProvider =>
{
    var configuration = serviceProvider.GetRequiredService<IConfiguration>();
    var databasePath = configuration["Launchpad:DatabasePath"]
        ?? Path.Combine(".", "data", "launchpad.db");
    return new LaunchpadStore(databasePath);
});

var app = builder.Build();
var store = app.Services.GetRequiredService<LaunchpadStore>();
await store.InitializeAsync();

app.Logger.LogWarning("NON-PRODUCTION TRUSTED-HEADER REFERENCE");

app.Use(async (context, next) =>
{
    context.Response.Headers[ApiContract.WarningHeaderName] = ApiContract.WarningHeaderValue;
    await next(context);
});

app.MapPost("/api/launch-requests", async (
    HttpRequest request,
    LaunchpadStore launchpadStore,
    CancellationToken cancellationToken) =>
{
    var body = await RequestValidation.ReadCreationAsync(request, cancellationToken);
    if (body.Problem is not null)
    {
        return ApiContract.Problem(body.Problem);
    }

    var identity = ReferenceIdentity.Parse(request.Headers);
    if (identity.ActorProblem is not null)
    {
        return ApiContract.Problem(identity.ActorProblem);
    }

    if (identity.RoleProblem is not null)
    {
        return ApiContract.Problem(identity.RoleProblem);
    }

    if (identity.Role != ReferenceRole.Requester)
    {
        return ApiContract.Problem(ApiContract.RoleMismatch());
    }

    try
    {
        var resource = await launchpadStore.CreateAsync(
            body.FeatureName!,
            identity.ActorId!,
            cancellationToken);
        return Results.Created($"/api/launch-requests/{resource.Id}", resource);
    }
    catch (SqliteException exception) when (LaunchpadStore.IsAvailabilityFailure(exception))
    {
        return ApiContract.Problem(ApiContract.DatabaseUnavailable());
    }
});

MapDecision(
    app,
    "/api/launch-requests/{id}/approvals/product",
    DecisionKind.ProductApproval);
MapDecision(
    app,
    "/api/launch-requests/{id}/approvals/ai-risk",
    DecisionKind.AiRiskApproval);
MapDecision(
    app,
    "/api/launch-requests/{id}/rejection",
    DecisionKind.Rejection);

app.MapGet("/api/launch-requests/{id}", async (
    string id,
    LaunchpadStore launchpadStore,
    CancellationToken cancellationToken) =>
{
    if (!RequestValidation.TryCanonicalGuid(id, out var requestId))
    {
        return ApiContract.Problem(ApiContract.InvalidRequestId());
    }

    try
    {
        var resource = await launchpadStore.GetAsync(requestId, cancellationToken);
        return resource is null
            ? ApiContract.Problem(ApiContract.RequestNotFound())
            : Results.Json(resource);
    }
    catch (SqliteException exception) when (LaunchpadStore.IsAvailabilityFailure(exception))
    {
        return ApiContract.Problem(ApiContract.DatabaseUnavailable());
    }
});

app.MapGet("/api/launch-requests/{id}/audit", async (
    string id,
    LaunchpadStore launchpadStore,
    CancellationToken cancellationToken) =>
{
    if (!RequestValidation.TryCanonicalGuid(id, out var requestId))
    {
        return ApiContract.Problem(ApiContract.InvalidRequestId());
    }

    try
    {
        var audit = await launchpadStore.GetAuditAsync(requestId, cancellationToken);
        return audit is null
            ? ApiContract.Problem(ApiContract.RequestNotFound())
            : Results.Json(audit);
    }
    catch (SqliteException exception) when (LaunchpadStore.IsAvailabilityFailure(exception))
    {
        return ApiContract.Problem(ApiContract.DatabaseUnavailable());
    }
});

app.Run();

static void MapDecision(WebApplication app, string path, DecisionKind kind)
{
    app.MapPost(path, async (
        string id,
        HttpRequest request,
        LaunchpadStore launchpadStore,
        CancellationToken cancellationToken) =>
    {
        if (await RequestValidation.HasBodyAsync(request, cancellationToken))
        {
            return ApiContract.Problem(ApiContract.BodyNotAllowed());
        }

        if (!RequestValidation.TryCanonicalGuid(id, out var requestId))
        {
            return ApiContract.Problem(ApiContract.InvalidRequestId());
        }

        try
        {
            var result = await launchpadStore.DecideAsync(
                requestId,
                kind,
                ReferenceIdentity.Parse(request.Headers),
                cancellationToken);
            return result.Problem is null
                ? Results.Json(result.Resource)
                : ApiContract.Problem(result.Problem);
        }
        catch (SqliteException exception) when (LaunchpadStore.IsAvailabilityFailure(exception))
        {
            return ApiContract.Problem(ApiContract.DatabaseUnavailable());
        }
    });
}

public partial class Program;
