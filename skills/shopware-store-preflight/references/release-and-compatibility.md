# Release and compatibility

## REL-01 — Inspect the shipped archive

Compare the archive root, technical name, PSR-4 mapping and `extra.shopware-plugin-class` with the bootstrap file, including case sensitivity.
Check actual runtime dependencies and shipped assets, not only the development checkout.
Remove credentials, repository metadata, test fixtures, temporary files and unused development artifacts from the release package.
Keep required readable JavaScript sources alongside production assets.
Do not delete generated files solely because they are unfamiliar: establish their purpose in the supported release tooling.
In particular, distinguish required checksum/build manifests and useful usage documentation from development caches; a filename-only blacklist can reject valid artifacts.

Verification: unpack the exact release, resolve the bootstrap and resources, inspect dependency delivery and compare source with compiled output.
Use current Store packaging guidance for exclusion decisions; a dependency's own legitimate runtime resource is not equivalent to an accidentally bundled development tree.

## REL-02 — Declare an honest version and dependency range

An API present on the latest patch may not exist on the oldest declared patch.
Check referenced classes, service IDs, method signatures, template blocks and Administration component props against the release range.
Either provide a working compatibility path or narrow the range.
A guard is ineffective if the guarded branch later references the missing class.
Do not invent convenience APIs or recommend methods solely from an old review comment.

Verification: validate the oldest supported release and newest supported stable release; inspect intermediate patch boundaries for changed APIs.
Do not add unused packages to silence unrelated diagnostics or copy historical wildcard/early-access examples into a current release.

## REL-03 — Build artifacts must match their sources

Inspect both authored source and the shipped bundle when feedback mentions stale behavior or debug output.
Rebuild after fixing source; stale bundles can preserve a rejected behavior.
Attribute bundled statements to their originating dependency before asking the author to remove them.

Verification: exercise the packaged assets, inspect browser errors and identify whether a flagged statement is authored code, generated scaffolding or bundled core code.

## REL-04 — Translations must work on the declared versions

Use an English fallback and translated user-facing settings, errors and JavaScript strings.
Choose snippet naming and registration conventions supported by the extension's version range; newer language-only naming is not automatically compatible with older releases.
Do not remove legacy registration without checking the minimum supported version.
Test a missing locale as well as the advertised languages.

## REL-05 — Advertise only working behavior

Trace each setting and major listing promise to implemented behavior.
Remove or implement unused retry switches, disabled-provider settings and configuration fields.
Examples belong in placeholders, not live defaults that contact a sample phone number or endpoint.
Check previews, icons, setup instructions and advertised languages against the submitted package.
Do not infer that a technical review establishes legal compliance, authorship or ownership.

## REL-06 — Namespace registrations and verify their wiring

Give new route paths and names, services, components, snippets and selectors an extension/vendor-specific identity where required to avoid collisions.
A prefixed route name does not prevent collision in an unprefixed path.
Intentional extension of an existing core component/block is different from registering a new generic identifier.
Check constructor arguments, DI definitions, imports, route loaders, subscribers and scheduled-handler bindings together.
Where Shopware exposes a public abstract route/decoration contract, depend on that supported contract rather than a concrete implementation that another extension can decorate.
An existing class or method is not useful if the framework never invokes it.
Missing services or broken route wiring can limit a suspected defect's demonstrated reachability; report that condition rather than asserting an exploitable endpoint already exists.

Verification: inspect resolved routes/container/handler registration in a suitable test environment and exercise the relevant entrypoint.

## REL-07 — Resolve actionable static-analysis and maintainability findings

Run the extension's applicable coding-standard and static-analysis checks against its supported dependencies.
Investigate unknown methods, missing service definitions, invalid field flags, unused dependencies and unreachable functionality before suppressing diagnostics.
Use typed configuration/request accessors when available, and keep service responsibilities understandable rather than embedding unrelated import, query and rendering logic in one controller.
Remove genuinely dead code and stale comments, but trace callers and generated registrations before deciding a symbol is unused.
Keep style/refactoring recommendations distinct from reproducible failures and explicit submission requirements.

Verification: rerun the relevant analysis after changes and exercise affected entrypoints; a textual match inside a comment or vendor bundle is not proof of a forbidden operation.

Policy references: [Code quality](https://developer.shopware.com/docs/guides/development/testing/store/code-quality.html), [common review errors](https://developer.shopware.com/docs/guides/development/testing/store/store-review-errors.html), [content and translations](https://developer.shopware.com/docs/guides/development/testing/store/content-and-translations.html).
