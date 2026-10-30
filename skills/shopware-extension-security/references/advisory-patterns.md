# Advisory patterns for extension developers

## Public baseline

The `shopware/shopware` repository advisory API returned 92 published, non-withdrawn advisories on 2026-10-22: 12 critical, 19 high, 38 medium, and 23 low. Refresh this snapshot with `scripts/advisories.py` before quoting counts.

The most frequent populated CWE fields were SSRF (`CWE-918`, 6), SQL injection (`CWE-89`, 5), code generation in templates (`CWE-1336`, 4), access control (`CWE-284`, 4), and code injection (`CWE-94`, 4). Many advisories have no CWE, so these counts understate authorization, isolation, and disclosure issues.

## Translate advisories into extension controls

Use these lineages to ask whether an extension recreates a known failure mode.

| Published lineage | Extension risk | Required control and regression test |
|---|---|---|
| Alternate writes and privilege escalation: `GHSA-243q-g9j3-qf6r`, `GHSA-v39m-97p8-gqg7`, `GHSA-gv8p-48fr-4fxg`, `GHSA-4wpv-5fvv-c3xp`, `GHSA-p589-2ff8-3wfw`, `GHSA-8xfc-pww7-3rm5` | A plugin protects one controller while generic CRUD, sync, clone, import, nested associations, or profile-style updates can still set privileged fields. | Put protection on the shared service, DAL field, or write-validation boundary. Test direct, nested, and generic write paths with a limited context. |
| DAL aggregation and query construction: `GHSA-qmp9-2xwj-m6m9`, `GHSA-p6w9-r443-r752`, `GHSA-8g35-7rmw-7f59`, `GHSA-q5qc-g5xc-2p8f`, `GHSA-p37c-pm9p-7vm5`, `GHSA-2qxr-vvj4-5934` | Extension routes accept arbitrary field paths, aliases, grouping, sorting, or identifiers and interpolate them into DBAL or custom SQL. | Prefer DAL; parameterize values and allowlist query structure. Test malformed, nested, and unsupported field paths without reading real secrets. |
| URL fetching and SSRF: `GHSA-gcvv-gq92-x94r`, `GHSA-7gm7-8q8v-9gf2`, `GHSA-3535-m8vh-vrmw`, `GHSA-3cpp-fv95-mpr5`, `GHSA-gq96-5pfx-f4vc`, `GHSA-fgjq-45xv-rj8r`, `GHSA-rrc3-p9vx-5373` | A plugin or app backend fetches merchant/customer URLs, images, documents, callbacks, or feeds using a raw HTTP client or validates only the initial hostname. | Use the current protected Shopware transport/validator where it applies. Enforce scheme and destination policy across DNS and redirects. Test loopback, private IPs, IPv6, and redirects with a local fake service. |
| Store API visibility and association traversal: `GHSA-f2vv-h5x4-57gr`, `GHSA-qg7c-q3vq-rgxr`, `GHSA-hhcq-ph6w-494g`, `GHSA-m895-2hj3-8cg9`, `GHSA-674c-5376-96rv`, `GHSA-7vvp-j573-5584` | Custom entities or extensions expose internal fields through `ApiAware`, associations, aggregations, exports, totals, or serialized extensions. | Minimize API-aware fields and apply scoping to every read form. Test root reads, associations, aggregations, export output, and partial field requests. |
| Twig and code-execution boundaries: `GHSA-93cw-f5jj-x85w`, `GHSA-7v2v-9rm4-7m8f`, `GHSA-27wp-jvhw-v4xp`, `GHSA-35jp-8cgg-p4wj`, `GHSA-7cw6-7h3h-v8pf`, `GHSA-6qhw-38wm-7g7h` | An extension renders user-controlled templates, uses `raw`, exposes callable helpers, or assumes the app-script sandbox covers custom bridges. | Keep templates static, pass data as values, preserve autoescaping, and expose narrow non-callable services. Test the final renderer with inert markers. |
| Media, uploads, and rendered files: `GHSA-fc38-mxwr-pfhx`, `GHSA-vrf2-xghr-j52v`, `GHSA-6wh5-mw9h-5c3w`, `GHSA-xvhc-gm7j-mhmc`, `GHSA-p67w-3mq7-rw2g` | Extension-controlled filename, path, extension, MIME, storage visibility, or later metadata update produces traversal, public disclosure, or browser execution. | Canonicalize and confine paths, generate storage names, validate content and intended use, preserve private storage, and serve active formats with safe headers. Test create and update separately. |
| Identity, recovery, and enumeration: `GHSA-w267-m9c4-8555`, `GHSA-hh7j-6x3q-f52h`, `GHSA-2w46-vq8h-98vh`, `GHSA-7w52-7jvm-m9vw`, `GHSA-gqc5-xv7m-gcjq`, `GHSA-8v9p-g828-v98f`, `GHSA-xj2c-8fw5-mr6m` | An extension adds login, magic links, API keys, OAuth callbacks, or password-like recovery without complete rotation, expiry, host validation, and indistinguishable responses. | Bind tokens to purpose and identity, expire and revoke them after trust changes, derive public URLs from configured trusted origins, and rate limit. Test response and timing behavior plus token reuse. |
| Session and cache isolation: `GHSA-h9q8-5gv2-v6mg`, `GHSA-jp6h-mxhx-pgqh`, `GHSA-6wrh-279j-6hvw`, `GHSA-r64m-qchj-hrjp`, `GHSA-c2f9-4jmm-v45m`, `GHSA-5297-wrrp-rcj7` | A storefront extension caches personalized output or allows one context token, cookie, header, host, or error response to influence another visitor. | Mark private responses correctly and vary or bypass cache for identity-dependent output. Test two identities sequentially, including errors and redirects. |
| Order, payment, and state boundaries: `GHSA-88rc-3p98-rgvx`, `GHSA-wq3r-jwrq-xg6w`, `GHSA-r2vg-hvjm-fg38`, `GHSA-9v5m-39wh-5chq`, `GHSA-f8q6-3g5w-jjr6` | A payment, shipping, document, cart, or order extension trusts IDs, current sales-channel settings, UI availability, or an allowed state-machine transition without checking ownership and business rules. | Re-read the target entity, bind it to the caller and original sales channel, validate current business state, and make mutations idempotent. Test foreign IDs, cross-channel requests, retries, and disallowed states. |
| Webhook ownership and event permissions: `GHSA-r432-q883-wgvf` | A plugin-created webhook or app subscription receives data beyond its owner/app permissions, can be repointed, or subscribes broadly to sensitive events. | Request only required manifest permissions and events, bind editable webhooks to an owner, and prevent privilege/target changes outside that owner. Test a limited role and a sensitive event. |

## How to use a lineage

1. Select the lineage closest to the extension feature.
2. State the invariant the extension must preserve.
3. Search the extension for every entry point that reaches the same sensitive effect.
4. Implement the control at the lowest shared boundary available to the extension.
5. Add one positive test and the strongest realistic negative test.

The extension does not need to copy Shopware's historical patch. Current Shopware APIs may offer a safer shared service or flag; inspect the supported version's implementation before choosing the fix.
