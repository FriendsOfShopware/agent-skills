# Channels, cache and jobs

## RUN-01 — Resolve channel configuration consistently

Pass the relevant sales-channel ID when resolving channel-scoped settings.
Define what global inheritance, explicit disablement, zero and empty values mean on each supported version.
Do not promise that a channel zero disables a global value without checking core inheritance semantics.
Use a separate enable/disable switch when values alone cannot express the intended behavior reliably.

Verification: two channels with different settings, global defaults, one disabled channel and both zero/empty overrides.

## RUN-02 — Preserve the appropriate context

Use the incoming sales-channel/customer/language/currency/version context for customer-facing behavior.
Do not introduce a default or system context merely to avoid permissions or missing data.
A deliberate fixed-language or system operation can be valid; explain its purpose and keep the scope narrow.
Confirm the actual supported context API before recommending a factory method.

## RUN-03 — Keep cache scope and invalidation correct

Identify all inputs to cached output, including channel, language, currency, customer permissions and relevant configuration.
Invalidate for the actual event and entity that changes the data; translated field changes may use translation events.
Do not disable the whole storefront cache to solve one feature's dynamic behavior.
Avoid non-silent high-frequency configuration writes that repeatedly invalidate broad cache tags where the supported API provides a suitable alternative.

Verification: warm caches, switch context, update source data, and confirm both isolation and refresh.

## RUN-04 — Bound work before loading entities

Filter and paginate in the query rather than loading everything and filtering in PHP.
Use ID-only queries or aggregations when no entity data is needed.
Avoid uncached repeated counts, N+1 reads and expensive wildcard scans on hot paths without a justified strategy.
A filter in PHP after a fixed batch can starve eligible rows indefinitely.

Verification: datasets larger than one batch, disabled-channel rows before eligible rows, empty batches, and realistic catalog sizes.
Do not label every SQL query or uncached lookup a performance defect without checking frequency and scale.

## RUN-05 — Queue remote or expensive work safely

Keep slow external requests out of checkout, registration and other latency-sensitive write flows when asynchronous execution fits the feature.
Make retries idempotent, use bounded payloads and record completion only after actual success.
Do not assume temporary system scope survives message serialization; re-establish only the privilege required by an authorized worker operation.
Define failure, retry and recovery behavior for stuck jobs.
Verify that messages are actually routed asynchronously; dispatch alone does not prove a worker handles them later.

Verification: timeout, duplicate delivery, worker restart, partial failure and local transaction rollback.

## RUN-06 — Coordinate tasks and concurrent changes

Register and remove tasks according to active/inactive lifecycle semantics.
Ensure removed extension classes cannot remain scheduled.
Delete or advance only the records actually processed, not records concurrently added behind a broad timestamp cutoff.
Use appropriate locking or atomic transitions for work that must not run twice.
Represent cancellation in extension-owned state rather than deleting transport-specific queue rows; installations can use different queue backends.

Verification: inactive update/uninstall, overlapping workers and newly committed records during a batch.

Policy references: [Functionality and integration](https://developer.shopware.com/docs/guides/development/testing/store/functionality-integration.html), [storefront performance and errors](https://developer.shopware.com/docs/guides/development/testing/store/storefront-performance-and-errors.html).
