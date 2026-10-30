---
name: shopware-extension-security
description: Securely build, review, and harden Shopware 6 extensions, including PHP plugins, apps, app backends, DAL entities, API routes, Administration modules, webhooks, Twig, media, and integrations. Use when implementing or auditing an extension for security; applies lessons from released Shopware advisories without turning the task into a core vulnerability hunt.
license: MIT
metadata:
  author: FriendsOfShopware
  version: "1.0.0"
  organization: FriendsOfShopware
  date: October 2026
  abstract: Practical security hardening for Shopware plugins and apps, informed by recurring vulnerability patterns in published Shopware advisories.
---

# Shopware Extension Security

Build and improve Shopware extensions so they preserve Shopware's authorization, data-isolation, input-validation, rendering, and secret-management boundaries. Use released Shopware advisories as regression lessons for extension code, not as the primary target of the review.

## Scope

Apply this skill when the user asks to:

- implement a security-sensitive feature in a Shopware plugin or app;
- review or harden an existing extension;
- fix a security finding in extension code;
- assess an app manifest, app backend, custom API route, DAL entity, webhook, Twig template, Administration module, upload, or external integration;
- add security regression tests to an extension.

Identify the extension model first. Plugins run inside Shopware and can reach the service container, filesystem, database, events, and request context. Apps run remotely or through sandboxed app features and rely on manifest permissions, signed communication, per-shop credentials, and API boundaries. Review hybrid extensions along both paths.

## Workflow

1. Locate the extension roots and supported Shopware versions from `composer.json`, `manifest.xml`, and lock files. Preserve existing repository instructions and conventions.
2. Inventory exposed surfaces before editing: routes, controllers, DAL definitions, subscribers, decorators, scheduled tasks, commands, migrations, Twig, JavaScript, manifest permissions, webhooks, action buttons, custom modules, app scripts, external endpoints, uploads, and outbound HTTP.
3. Define the assets and actors for each surface: anonymous visitor, customer, limited administrator, integration, app, background worker, or another tenant/shop.
4. Read [references/extension-review.md](references/extension-review.md) and inspect only the sections that match the extension type and changed feature.
5. Read [references/advisory-patterns.md](references/advisory-patterns.md) when the feature touches authorization, DAL queries, templates, media, URL fetching, identity, sessions, caching, or checkout state.
6. Trace untrusted input to its sensitive effect. Verify server-side permission, ownership, sales-channel, shop/tenant, state, and field-level decisions at the shared boundary rather than relying on UI visibility or one controller.
7. When the user requests an improvement or fix, implement the smallest complete remediation. Avoid returning only a checklist when the code can be safely corrected in scope.
8. Add focused tests using [references/remediation-and-tests.md](references/remediation-and-tests.md). Include an authorized case and the strongest realistic unauthorized or malformed case.
9. Run the extension's relevant checks. Report changed behavior, evidence, remaining risks, and any supported Shopware versions or configurations that were not exercised.

## Required Security Properties

- Grant the extension and its users only the permissions the feature requires. Enforce permissions in backend routes and services; Administration ACL visibility is a user-interface control.
- Bind every customer, order, cart, document, media, webhook, and app-backend record to the correct owner, sales channel, context, or shop. Never accept that binding solely from client input.
- Keep sensitive and system-controlled DAL fields out of unintended APIs. Apply field or entity write protection at a layer shared by generic CRUD, Sync API, imports, nested writes, and custom controllers.
- Prefer DAL and parameterized DBAL queries. Allowlist any identifier, field path, sort, or aggregation shape because SQL parameters protect values, not query structure.
- Verify app signatures against the exact raw body or canonical query expected by Shopware, use constant-time comparison, enforce freshness, prevent replay for state-changing events, and select secrets by the authenticated shop identity.
- Escape output for its final context. Treat Twig `raw`, dynamic template source, HTML sanitization, Administration HTML injection, SVG/HTML media, PDF generation, and email rendering as separate sinks.
- Validate outbound destinations at connection time and across redirects. Reuse the current Shopware-provided protected transport or validator where applicable; do not create a weaker extension-local URL check.
- Keep secrets out of DAL API responses, browser bundles, logs, exceptions, caches, and exported files. Rotate or revoke credentials and recovery artifacts when their trust basis changes.
- Validate business state where the mutation occurs. A disabled button, hidden Administration route, or storefront condition does not constrain direct API requests.
- Fail closed. Signature, permission, ownership, validation, and dependency failures must not silently fall back to privileged or unscoped behavior.

## Advisory Data

The bundled `scripts/advisories.py` helper refreshes published `shopware/shopware` advisories for pattern research:

```bash
python3 scripts/advisories.py --format stats
python3 scripts/advisories.py --search "access control"
```

Use the helper when a concrete extension surface needs historical examples. Do not require a full advisory analysis for routine extension changes.

## Deliverable

For an implementation task, return the hardened code and tests. For a review-only task, return prioritized findings with code locations, exploit preconditions, concrete impact, and an actionable fix. Distinguish confirmed behavior from untested or history-based inference.
