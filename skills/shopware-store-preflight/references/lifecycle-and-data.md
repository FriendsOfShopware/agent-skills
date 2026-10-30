# Lifecycle and data

## DATA-01 — Test the complete lifecycle

Exercise fresh install, activation, update while active and inactive, deactivation, both uninstall choices and reinstall.
Check the context of a user allowed to manage extensions but without arbitrary entity permissions.
Use narrowly scoped system privileges for necessary lifecycle writes where the supported core requires them; do not globally elevate normal requests.
Validation subscribers must tolerate legitimate lifecycle deletes and null-valued configuration batches.

Verification: repeat transitions and inspect database state, files and task registrations, including after removing the extension files.

## DATA-02 — Define cleanup ownership and preservation

Inventory tables, custom fields, associations, templates, media, configuration keys and scheduled tasks created by the extension.
Respect keep-data behavior.
For complete removal, remove extension-owned data while preserving business-critical records and data owned by other extensions.
Deactivate referenced payment/shipping methods when deletion would damage business history.
Do not infer ownership solely from a loose name substring.

Core can remove declared `config.xml` settings automatically; dynamically written token/configuration keys may require explicit cleanup.
Verify the supported core behavior rather than requiring either universal manual deletion or universal reliance on core.

## DATA-03 — Respect foreign keys and deletion order

Model persistent business entities with the DAL and appropriate relations where applicable.
Follow actual foreign-key behavior: `SET NULL` does not delete child records, and `RESTRICT` can require deleting dependants first.
Check versioned references and patch-specific schema changes.
Do not assume raw row deletion also cleans physical files or related entities.

Verification: remove parent records with dependants and inspect for orphans; verify both fresh installs and upgrades from shipped versions.

## DATA-04 — Use the DAL without inventing an absolute SQL ban

Prefer repositories and supported services for ordinary core-entity CRUD so events, validation, indexing and permissions stay intact.
Investigate raw SQL for bypassed lifecycle behavior, missing scope and data-integrity hazards.
Migrations, specialized aggregations and carefully justified cleanup can need DBAL/SQL.
For example, a merge-based JSON update may not remove an existing key: verify removal semantics before replacing a targeted cleanup operation.
Keep parameters bound and identifiers constrained.

## DATA-05 — Manage media as a lifecycle, not just an upload

Associate uploads with an extension-owned media folder and records.
Register legitimate media usage with the relevant core mechanism so unused-media cleanup does not delete live assets.
Enforce cumulative limits, avoid orphan uploads after failed saves and delete owned files when required on uninstall.
Use storage services that work with remote adapters instead of assuming a local `public/` path.

Verification: save failures, repeated submissions, unused-media cleanup, delete-data uninstall and remote-storage behavior.

## DATA-06 — Preserve migration and transaction correctness

Keep already-released migrations stable; add forward migrations for updates.
Make fresh-install and upgrade paths reach the same intended schema.
Check transactional boundaries when an entity-written subscriber writes back to that entity or calls an external system.
Do not mark external work complete before the local transaction and response semantics establish success.

Policy reference: [Uninstallation and data cleanup](https://developer.shopware.com/docs/guides/development/testing/store/installation-and-cleanup.html).
