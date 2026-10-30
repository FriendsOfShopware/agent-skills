# Extension security review

## Start with an inventory

Determine whether the repository contains a PHP plugin, static plugin, app, remote app backend, theme, or a combination. Record supported Shopware and PHP versions and find all externally reachable or privileged components.

Useful discovery targets include:

```text
composer.json
manifest.xml
src/**/*Controller.php
src/**/*Route.php
src/**/*Definition.php
src/**/*Subscriber.php
src/**/*Command.php
src/**/*Handler.php
src/Resources/config/routes.php
src/Resources/config/services.*
src/Resources/views/**/*.twig
src/Resources/app/administration/**/*
Resources/scripts/**/*.twig
Resources/views/**/*.twig
migrations and dependency lock files
```

Follow repository-specific instructions before running commands or editing files.

## PHP plugins

### Routes and authorization

- Give every route the correct route scope and explicit HTTP methods.
- For Admin API routes, enforce server-side ACL with `PlatformRequest::ATTRIBUTE_ACL`; hiding an Administration route, menu, or button is insufficient because direct API calls remain possible.
- Treat Store API and storefront callers as untrusted even when they possess a sales-channel access key or context token.
- Load the target entity server-side, then verify customer ownership, sales-channel binding, version, and allowed state. Do not trust an `ownerId`, `customerId`, `salesChannelId`, price, or privilege copied from the request.
- Put rules used by multiple routes in a shared domain service. Confirm subscribers, commands, workers, importers, and generic entity writes cannot bypass it.
- Use non-GET methods for mutations and preserve the framework's authentication, cookie, and cross-site request protections.

### DAL entities and repositories

- Add `ApiAware` only to fields and sources that must be exposed. Remove API visibility from secrets, internal status, raw payloads, credentials, and privileged metadata.
- Add `WriteProtected` or write validation for server-controlled fields. Choose allowed scopes deliberately and test generic Admin API, Sync API, nested association, import, and custom-controller writes.
- Review every association as a possible read and write path. Root repository decoration does not automatically prove association or aggregation safety.
- Scope criteria by the authenticated customer, sales channel, owner, or tenant before executing the query. Filtering returned results afterward can leak counts, aggregates, or side channels.
- Bound page size, nesting, and expensive filters. Validate extension-defined field names and aggregation types against allowlists.
- Prefer DAL repositories. With DBAL, bind all values and allowlist identifiers and SQL fragments; never concatenate request data into structural SQL.
- Keep migrations deterministic. Do not execute input-derived SQL, paths, or shell commands during install/update/uninstall.

### Services, subscribers, workers, and commands

- Assume messages and events can be retried, reordered, duplicated, or emitted for draft versions. Make side effects idempotent and validate current entity state.
- Do not elevate to `Context::SYSTEM_SCOPE` merely to avoid permission failures. If system context is required for background work, reconstruct and validate the initiating authority or store a narrowly scoped intent.
- Restrict CLI and scheduled-task inputs before file, process, network, or query use. Do not log access tokens, app secrets, customer data, full webhook payloads, or password/recovery material.
- When decorating a Shopware service, preserve its authorization, validation, transaction, and exception behavior unless the change deliberately strengthens it.

### Outbound HTTP, files, and media

- Treat URLs from configuration, customers, feeds, imports, and DAL fields as untrusted. Reuse the supported Shopware service such as the current URL validator/protected transport when it fits the use case.
- Enforce HTTPS where appropriate and validate the connected destination across DNS resolution and redirects. Extension-local regexes and a one-time hostname lookup do not prevent SSRF.
- Set connect, response, and total timeouts plus response-size limits. Do not forward Shopware cookies, authorization headers, or internal metadata to arbitrary destinations.
- Confine paths after canonicalization, generate storage names, and validate content separately from extension and declared MIME.
- Keep private media and documents private in every storage adapter. Authorize downloads and serve active formats such as HTML or SVG with restrictive headers and safe disposition.

### Twig, storefront, and Administration

- Keep template source static. Pass untrusted values as data and preserve context-aware escaping.
- Avoid `raw`, dynamic includes, dynamic callable names, and custom helpers that expose general service-container, filesystem, process, HTTP, or PHP-callable access.
- When HTML is an intentional feature, use the current Shopware sanitizer with a narrow policy and still encode for the final HTML, attribute, URL, JavaScript, email, or PDF context.
- Treat Administration JavaScript as attacker-observable client code. Do not ship secrets or rely on component ACL checks for backend authorization.
- Avoid `innerHTML` and unsafe URL insertion. Validate `postMessage` origin and sender for embedded content and constrain iframe origins.
- Review personalized storefront responses and errors for cache privacy, cookies, context tokens, and proxy-controlled headers.

## Apps and remote app backends

### Manifest and permissions

- Validate `manifest.xml` against the schema supported by the target Shopware versions.
- Request the smallest entity permissions and webhook events needed by current features. Remove historical or speculative permissions.
- Review `registrationUrl`, modules, action buttons, webhooks, payment/tax/shipping endpoints, and allowed hosts as network trust boundaries. Use HTTPS and stable, controlled origins in production.
- Treat app scripts and custom templates as sandboxed but still minimize data access, output, loops, and side effects.

### Signed requests and tenant isolation

- Verify `shopware-shop-signature` over the exact raw body or query representation required by that endpoint before parsing or acting.
- Use constant-time signature comparison. Select the secret through a stable shop identifier and confirm that the signed shop identity matches the credential record.
- Enforce a short timestamp window where Shopware provides a signed timestamp. Deduplicate state-changing webhooks with the signed shop identity plus `eventId` or another stable request identifier.
- Store credentials per shop, encrypted at rest when the platform allows it. Never accept a request-supplied shop URL as sufficient tenant identity or overwrite credentials without the authenticated registration/rotation flow.
- Scope every database lookup and job to the authenticated shop. Unique constraints should include tenant identity where identifiers are only unique within a shop.
- On uninstall, disable future work and remove or anonymize credentials and merchant data according to the extension's retention obligations.

### App API and browser communication

- Use app credentials only on the backend. Do not expose the app secret, Admin API secret, or unrestricted bearer tokens to storefront or Administration JavaScript.
- Validate Shopware-issued client-side app JWT signatures, issuer/shop binding, expiry, and required claims. Treat a missing optional claim as no permission.
- Configure CORS for known shop or module origins and required methods/headers. Avoid credentialed wildcard origins.
- For action buttons and modules, verify the signature and then authorize the requested operation; a signed request proves Shopware origin, not that every selected entity or state transition is valid for the extension's business rule.
- Sign responses when the Shopware app protocol requires it. Restrict redirect and iframe URLs to trusted destinations.

### Webhooks and external providers

- Subscribe only to required events and permissions. Use `onlyLiveVersion` when draft-version events would create duplicate or premature side effects.
- Expect retries and out-of-order delivery. Make handlers idempotent, record processing atomically, and fetch current state when the event contains identifiers rather than a complete entity.
- Authenticate callbacks from payment, shipping, tax, and other providers independently of the Shopware request signature. Bind callback references to the correct shop, order, transaction, and expected state.
- Do not trust prices, payment status, refund amounts, or redirect destinations returned by the browser.

## Dependencies and operational behavior

- Review Composer and npm dependencies that execute in production, including abandoned packages, unsafe scripts, and known advisories relevant to reachable code.
- Keep supported Shopware constraints explicit and test the oldest and newest supported release lines when security APIs differ.
- Ensure production does not enable development bypasses for URL validation, debug output, permissive CORS, test keys, or insecure transport.
- Return generic client errors and log structured diagnostics without secrets or personal data.
- Document required permissions, outbound hosts, stored data, retention, and operational security settings for merchants.
