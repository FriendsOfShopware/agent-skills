# Storefront and Administration

## UI-01 — Extend existing rendering points

Confirm the parent template and overridden block actually exist and are used on every supported version.
Prefer the narrowest suitable block and preserve parent behavior where required.
Test CMS-based product pages, account pages and other changed rendering paths rather than assuming a legacy template still executes.

Verification: render the feature in a real request with relevant layouts and assert the visible behavior, not merely that the Twig file parses.

## UI-02 — Use platform JavaScript and component lifecycles

Register storefront behavior through the supported plugin system and compile assets with the extension.
Use Administration reactivity, computed values and supported component extension points for Vue-managed UI.
Avoid polling or direct DOM mutations that fight component updates.
Vue's virtual DOM is not Shadow DOM; do not repeat that incorrect explanation from historical feedback.
Use supported lifecycle extension conventions for the targeted Administration version.
Check that an extracted `createdComponent()` method is actually invoked by the component's lifecycle; renaming a hook without wiring it can disable initialization.

Verification: navigation, repeated initialization, asynchronous rerender and component teardown.

## UI-03 — Communicate state and errors truthfully

Show failed saves and API errors; empty catch blocks must not leave users believing work succeeded.
Use appropriate loading, disabled, success and empty states.
Prevent stale asynchronous responses from applying to a newly selected customer or record.
Keep pagination, counts and aggregates consistent with the complete result set.
A limited list of recent reviews cannot establish an all-time average.

## UI-04 — Integrate consent with the actual runtime

Register non-essential cookies with Shopware's consent mechanism in an appropriate category.
Declaring a cookie is insufficient if tracking or an embedded external service starts before the relevant consent.
Handle withdrawal and avoid substituting a cosmetic independent consent bar for the platform's mechanism.
Check which cookie-provider APIs exist on the oldest declared release.

Verification: new visitor, accept, decline, withdraw and reload; inspect both network requests and storage.
Use current policy and the actual feature purpose when determining required versus optional behavior.

## UI-05 — Preserve indexing and structured data

Keep public content canonical and discoverable where appropriate.
Mark private, tokenized, utility and otherwise non-indexable routes appropriately, including error responses.
Do not expose customer information through a supposedly harmless review/preview landing page.
Keep product structured data valid, with special attention to missing reviews, availability and duplicate markup.

Verification: response headers/meta, representative page markup and before/after structured-data validation.
Do not apply a blanket no-index rule to ordinary public extension content.

## UI-06 — Keep presentation scoped and accessible

Use extension classes and compiled styling without broadly overriding core UI.
Prefer maintainable selectors over indiscriminate `!important` and inline styling.
Check mobile/tablet/desktop, keyboard use, labels and meaningful image alternatives.
Keep non-content chrome from distorting heading structure.
Remove unrelated advertising, hidden backlinks and live demo content from merchant-facing output.

Verification: representative storefront and Administration pages before and after activation; inspect console errors, layout and changed interactions.

Policy references: [Storefront performance and errors](https://developer.shopware.com/docs/guides/development/testing/store/storefront-performance-and-errors.html), [SEO and structured data](https://developer.shopware.com/docs/guides/development/testing/store/seo-and-structured-data.html), [cookies and privacy](https://developer.shopware.com/docs/guides/development/testing/store/cookies-and-privacy.html).
