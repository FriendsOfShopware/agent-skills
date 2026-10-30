# Integrations and observability

## INT-01 — Provide a usable connection check

Validate external credentials on save or through a test action, and show an actionable status.
Use shared injectable HTTP clients/services with bounded timeouts and deliberate error handling.
Treat remote failure as an expected state, including missing configuration and unavailable services.
Catch exceptions at a meaningful recovery boundary and verify the fallback works end-to-end; neither swallowing all failures nor banning every broad catch is a sound rule.
Avoid doing configuration reads and remote setup in constructors when they create hidden work on ordinary service instantiation.

Verification: valid/invalid credentials, timeout, malformed response and service unavailability.
Check whether API success can legitimately be represented by an empty/null result before recording completion.

## INT-02 — Use the Administration API service infrastructure

Use the supported API client abstraction for normal Administration requests rather than repeatedly constructing bearer headers and bypassing common error/authentication handling.
Display server failures and preserve meaningful response details, including JSON errors returned where a download expects a Blob.
Do not replace a genuinely external integration protocol with the Admin API solely to satisfy a generic pattern.

## INT-03 — Isolate and bound extension logging

Use the supported extension-specific logger/channel and file configuration under the shop's logging directory.
Check the actual handler output: injecting a logger is not proof of the final filename or destination.
Avoid dumping credentials, customer data, full filenames or stack traces without a justified diagnostic need.
Define cleanup/retention for custom database logs and ensure failures do not create unbounded growth.

Verification: trigger a representative error, inspect its destination and redaction, and test cleanup with old rows.

## INT-04 — Respect storage abstractions

Use Shopware filesystem/media services for their supported storage domain.
Avoid `getcwd()` and assumptions about local public directories where CLI, relocated document roots or remote adapters change the layout.
Constrain downloads and uploads, handle failures, and remove temporary artifacts.

Verification: web versus CLI execution and the storage adapters the extension claims to support.

## INT-05 — Preserve external and cross-extension data semantics

Check third-party schemas and state machines against their supported versions.
A scheduled cancellation is not necessarily a completed cancellation; local deletion must not leave an external subscription charging.
Deleting a database row may leave a third-party file behind.
Use integration services when available and report skipped/unsupported sources rather than silently claiming a complete export or deletion.

Verification: representative third-party states, inactive dependencies, child records and retry behavior.
Do not invent retention periods or legal requirements from a single review example.

Policy references: [Functionality and integration](https://developer.shopware.com/docs/guides/development/testing/store/functionality-integration.html), [code quality and logging](https://developer.shopware.com/docs/guides/development/testing/store/code-quality.html#error-messages-and-logging).
