# Commerce and payments

## COM-01 — Preserve Shopware price semantics

Use the active currency, tax state, rounding and applicable rules when calculating or displaying prices.
Keep storefront, cart, checkout and order values consistent, including reference/list/regulation-price metadata when affected.
Do not assume raw gross product prices are valid for every sales channel or customer.
Combine this with SEC-08: trusted inputs and correct commercial calculations are separate requirements.

Verification: gross/net/tax-free contexts where supported, multiple currencies, quantities, rules, variants and discount combinations.

## COM-02 — Respect recalculation boundaries and order snapshots

Re-evaluate eligibility and quantities when the cart is recalculated; do not permanently trust an earlier payload.
Check whether processors also run during Administration order editing.
Preserve placed-order commercial snapshots where changing them would rewrite the agreed transaction.
Follow supported cart/Store API extension points so headless and normal storefront behavior agree where the extension claims to support both.

Verification: change quantity and customer state, remove a triggering product, recalculate and edit an existing order.

## COM-03 — Apply availability restrictions to every relevant surface

Hiding a product in one template does not restrict direct product, Store API, cart, search or export access.
Use sales-channel-aware entities and enforce the intended restriction at appropriate backend boundaries.
Trace listing, search/suggest, detail, cart, sitemap and exports as applicable to the claim, including supported search backends.

Verification: request a restricted product directly and through alternative entrypoints with allowed and forbidden customers/channels.

## COM-04 — Authenticate and reconcile payment callbacks

Verify callback authenticity, resource identity, amount/currency and the intended order transaction before changing payment state.
Reject empty/missing credential cases and use the correct channel's credentials.
Use stable technical state identifiers rather than translated labels.
Preserve supported core finalization and replay protections.

Verification: invalid signatures, wrong transaction/amount/channel and repeated callbacks.

## COM-05 — Make external financial side effects recoverable

Establish idempotency before a remote capture, refund or order creation, not only with a local uniqueness check afterward.
Handle the case where remote work succeeds but the local write fails.
Use reconciliation or compensation appropriate to the provider and expose a meaningful recoverable failure state.
Do not turn a failed persistence step into success unless the fallback actually preserves the required business outcome.

Verification: duplicate delivery, concurrent attempts, remote success/local failure and retry after interruption.

Policy references: [Functionality and integration](https://developer.shopware.com/docs/guides/development/testing/store/functionality-integration.html), [not allowed Store behaviors](https://developer.shopware.com/docs/guides/development/testing/store/not-allowed-store-behaviors.html).
