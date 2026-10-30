# Permissions and input

## SEC-01 — Match server permissions to the operation

For each custom Admin API route, identify the read or write operation and enforce appropriate privileges server-side.
Authentication alone does not authorize imports, email sending, deletion or configuration changes.
A broad read privilege such as `system_config:read` is not a suitable substitute for a write privilege.
Check that the selected privilege actually exists and maps to the required DAL operations.
Trace downstream DAL read/write validation and any context elevation before claiming a permission bypass: a mismatched route guard can be a design/usability defect while the repository still rejects the mutation.

Verification: call the route as a full administrator, intended restricted role, unrelated viewer and unauthenticated caller.
Inspect standard DAL endpoints too: protecting a custom controller is insufficient if the same sensitive mutation remains available through an entity API.

## SEC-02 — Make Administration UI permissions consistent

Register roles and gate navigation, routes, buttons and editable fields consistently with server permissions.
Ensure intended restricted users can use the feature without full admin rights.
Hiding a button is a usability measure, not an authorization boundary.
Avoid adding broad configuration privileges merely to make a small UI lookup succeed.

Verification: test both allowed and forbidden operations with the actual restricted role.

## SEC-03 — Scope storefront data to the current customer and channel

Resolve ownership from a trusted context, not a submitted customer or order ID.
Check sales channel, customer state and operation eligibility before reading or changing data.
Guest customers can have customer IDs; distinguish guests using the relevant customer state rather than null-ID assumptions.
Signed links need integrity, expiry and operation-specific authorization; login alone does not prove ownership.
Custom integration credentials must be unique or explicitly configured, not shared shipped defaults; reject missing/empty secrets and verify fresh-install and upgrade behavior.

Verification: change entity IDs, use another account/channel, test guest orders and test expired, invalid or reused links.

## SEC-04 — Preview and editor modes require a real trust boundary

A query parameter or client-controlled cookie must not expose drafts, enable compilation or weaken frame/security headers.
Authenticate and authorize preview access, constrain signed preview links and keep unpublished content out of public fallbacks.
Restrict cross-window messages to intended origins and validate their content; a caller-supplied `source` string is not authentication.

Verification: request preview URLs without admin credentials, tamper with layout IDs and exercise draft/live fallbacks.

## SEC-05 — Validate shapes, bounds and output contexts

Use typed request accessors where available, then validate domain constraints server-side.
Check array versus scalar shape, UUIDs, lengths, ranges, dates, enums, upload limits and allowed state transitions.
Browser validation alone cannot protect an endpoint.
Escape text in its output context; do not use Twig `raw` for ordinary text settings.
Rich-text fields need an intentional sanitization/rendering strategy rather than silently stripping promised formatting.
Neutralize spreadsheet formula injection when exporting attacker-controlled cells.

Verification: submit malformed arrays, overlong strings, invalid dates and forbidden enum values; verify controlled errors rather than uncaught exceptions.

## SEC-06 — Constrain interpreters, files and outbound requests

Do not expose arbitrary SQL, shell commands, file access or unsandboxed templates through a configuration UI.
Use an appropriate sandbox and allow-list for user-authored template features; string blocklists are not a language sandbox.
Validate file paths, redirects and outbound targets according to the feature's trust boundary.
For user-influenced outbound requests, restrict schemes and destinations, validate resolved addresses and redirects, retain TLS verification and reject inappropriate private/loopback/link-local targets.
Do not ban an intentional trusted-admin scripting feature solely for containing scripts; assess authorization, scope and the actual execution boundary.
When a custom authentication protocol is necessary for an integration, assess its design and accepted integration constraints; do not replace it mechanically with an incompatible protocol.

## SEC-07 — Exclude credentials from exports and logs

An all-columns export can expose passwords, tokens, hashes and secrets, including nested legacy/raw payloads.
Use an explicit export schema or effective recursive redaction strategy appropriate to the data model.
Do not assume a privacy export makes credentials safe to disclose.
Verify downloadable outputs and logs with representative sensitive fields.

## SEC-08 — Recalculate commercial values from trusted data

Prices, discounts, credit balances and entitlement limits must be derived from trusted server-side configuration and entities.
A calculation executed in PHP is still client-controlled if its input rates or surcharges came from a submitted payload.
Validate product eligibility and ownership, then recompute authoritative totals rather than trusting a stored copy of browser values.
Protect redemption and assignment against concurrent requests with appropriate atomic writes or uniqueness constraints.

Verification: tamper with quantities, rates, surcharges and identifiers; repeat or race the same redemption and verify the final financial state.

## SEC-09 — Keep safe requests free of mutations

Use an appropriate mutation method and target-version-supported request protections for state-changing actions.
Distinguish an explicit acceptance/redemption/confirmation from incidental request logging or view analytics; logging on GET alone is not evidence of a business-operation authorization flaw.
Emailed links can be visited by security scanners, crawlers and prefetchers: use a read-only landing page before an irreversible confirmation.
Do not prescribe removed legacy CSRF APIs to newer Shopware releases.

Verification: request the link without a user gesture and verify it does not send, redeem, delete or confirm anything.

Policy reference: [Not allowed Store behaviors](https://developer.shopware.com/docs/guides/development/testing/store/not-allowed-store-behaviors.html).
