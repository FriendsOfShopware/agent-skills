# Remediation and security tests

## Improve the code, not only the finding list

When the user asks to improve or fix an extension:

1. Identify the shared boundary that should enforce the rule.
2. Patch that boundary and all independently reachable paths in scope.
3. Preserve intended authorized behavior.
4. Add tests that prove both denial and success.
5. Run the narrow relevant suite, then the repository's normal quality checks when practical.

For a review-only request, do not mutate the repository. Provide concrete fixes and test cases instead.

## Prioritize findings

Prioritize by demonstrated impact and reachability:

1. Unauthenticated or customer-reachable code execution, SQL injection, credential compromise, cross-shop access, payment manipulation, and broad personal-data disclosure.
2. Low-privilege administration escalation, SSRF, private-file exposure, stored XSS in privileged contexts, and foreign-order or document access.
3. Missing defense in depth, overbroad permissions, enumeration, denial of service, and configuration weaknesses with meaningful conditions.

Do not inflate severity from a theoretical chain. Record required permissions, configuration, interaction, and affected data precisely.

## Test matrix

Select tests that observe the protected effect, not only an HTTP status.

| Boundary | Required negative case | Positive/control case | Strong observation |
|---|---|---|---|
| Admin API ACL | limited role calls route directly | role with exact privilege | response denied and no row, event, file, or job created |
| Ownership/sales channel | foreign customer/order/media ID and cross-channel context | owning identity and original channel | foreign data absent and state unchanged |
| DAL protected field | generic, sync, nested, and custom write attempts | trusted system path | protected value unchanged for every untrusted path |
| Store API visibility | root, association, aggregation, partial field, and export reads | allowed public field | sensitive value and derived counts absent |
| SQL/query shape | malformed and unsupported identifiers/aggregations | allowlisted query | query structure fixed and out-of-scope fixture not returned |
| App signature | missing, altered, wrong-shop, stale, and replayed request | valid fresh signed request | no side effect before verification; replay is idempotent or rejected |
| Multi-shop backend | valid credential from shop A with shop B identifier | matching shop and record | no cross-shop lookup, mutation, job, or response |
| SSRF | loopback/private/IPv6/redirect target | controlled public fixture | forbidden fake service receives no connection |
| Upload/path | traversal name, misleading MIME/extension, metadata update | valid expected media | path remains confined and response uses safe headers |
| XSS/rendering | context-specific inert markup marker | ordinary text/allowed HTML | marker remains text or is removed in final rendered response |
| Cache/session | two identities, logout/reset, error and redirect responses | same identity cache hit | identity B never receives A's body, headers, cookie, or token |
| Commerce state | foreign ID, retry, cross-channel request, disallowed state | valid current transition | order/payment/inventory side effects remain consistent |

Use rolled-back database fixtures and fake local transports. Never use live credentials, customer data, public targets, destructive shell payloads, or uncontrolled outbound requests.

## Fix patterns

- Move authorization from UI-only or route-only checks into the service performing the mutation, while retaining route ACL for early rejection.
- Move field protection into DAL flags or write validation that covers generic and nested writes.
- Replace post-query filtering with scoped `Criteria` or repository rules so counts and aggregations cannot leak.
- Replace dynamic SQL identifiers with a closed mapping from supported request values to known fields or expressions.
- Replace raw HTTP clients with the supported validated transport and apply time, size, redirect, and destination limits.
- Replace client-provided ownership or tenant identifiers with values derived from authenticated context.
- Replace dynamic template source and `raw` output with static templates, structured data, sanitization where HTML is required, and final-context encoding.
- Replace non-idempotent webhook processing with an atomic event record and a uniqueness key containing the authenticated shop identity.
- Replace broad app permissions and subscriptions with the minimal set exercised by current features.

## Review output

For each unresolved finding provide:

```text
Title:
Severity and confidence:
Affected component and versions:
Actor and prerequisites:
Security property violated:
Root cause and code locations:
Concrete impact:
Closest published Shopware pattern, if relevant:
Recommended fix boundary:
Regression tests:
Untested assumptions:
```

For completed fixes, lead with the new behavior, list the modified boundary and tests, and disclose material limitations. Avoid dumping a generic security checklist after the concrete result.
