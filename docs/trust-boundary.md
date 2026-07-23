# Trusted-header boundary

> **NON-PRODUCTION TRUSTED-HEADER REFERENCE:** caller-supplied headers are not authentication.

AI Feature Launchpad demonstrates actor-aware governance without implementing production identity.
The process accepts two headers as assertions from a hypothetical trusted upstream:

- `X-Reference-Actor-Id`;
- `X-Reference-Actor-Role`.

There is no actor directory or allow-list. A syntactically valid actor ID is trusted inside this
reference boundary. A missing, repeated, or invalid actor fails `401`. A missing, repeated, unknown,
or command-mismatched role fails `403`.

## Safeguards against misuse

- The host starts only when the ASP.NET Core environment is exactly `Development` or `Testing`.
- Startup logs `NON-PRODUCTION TRUSTED-HEADER REFERENCE`.
- Every HTTP response, including errors, carries:

  `X-Reference-Authentication-Warning: NON-PRODUCTION; caller-supplied headers are not authentication`

- Public examples repeat the warning before showing headers.
- The implementation contains no OAuth, JWT, cookie, API key, forwarded-header trust inference, or
  identity-provider integration.

The two GET routes intentionally consume no identity. They are observability surfaces for this local
reference and do not establish a confidentiality or read-authorization policy.

## What production would require

A production system would need an authenticated upstream, transport trust, issuer and audience
validation, credential lifecycle, authorization policy, data protection, operational monitoring,
deployment controls, and threat analysis. Those concerns are explicitly outside this reference and
must not be inferred from its headers or warning guard.
