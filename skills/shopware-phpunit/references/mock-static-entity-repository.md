---
title: Use StaticEntityRepository Instead of Mocking EntityRepository
impact: HIGH
impactDescription: Eliminates brittle repository mocks and provides realistic write tracking
tags: mock, repository, static-entity-repository, unit-test
---

## Use StaticEntityRepository Instead of Mocking EntityRepository

Shopware provides `StaticEntityRepository` as a drop-in replacement for `EntityRepository` in unit tests. It accepts predefined search results and records all write operations (`create`, `update`, `upsert`, `delete`) for assertion. This avoids complex `createMock()` setups and produces more readable, maintainable tests.

**Incorrect (manually mocking EntityRepository):**

```php
public function testMyService(): void
{
    $repository = $this->createMock(EntityRepository::class);
    $repository->method('search')->willReturn(
        new EntitySearchResult(
            'product',
            1,
            new EntityCollection([$product]),
            null,
            new Criteria(),
            Context::createDefaultContext()
        )
    );
    $repository->expects(static::once())->method('update');

    $service = new MyService($repository);
    $service->doSomething(Context::createDefaultContext());
}
```

**Correct (using StaticEntityRepository):**

```php
use Shopware\Core\Test\Stub\DataAbstractionLayer\StaticEntityRepository;

public function testMyService(): void
{
    $product = new ProductEntity();
    $product->setId(Uuid::randomHex());
    $product->setName('Test');

    $repository = new StaticEntityRepository([
        new EntityCollection([$product]),
    ]);

    $service = new MyService($repository);
    $service->doSomething(Context::createDefaultContext());

    // Assert writes happened with correct data
    static::assertCount(1, $repository->updates);
    static::assertSame('new-name', $repository->updates[0][0]['name']);
}
```

### Constructor

The constructor accepts two arguments:

- `$searches` — An array of results consumed in order by `search()` and `searchIds()`. Each entry can be:
  - An `EntityCollection` or array of entities — wrapped into an `EntitySearchResult` automatically
  - An `EntitySearchResult` — returned as-is
  - An `AggregationResultCollection` — returned as an empty result with aggregations
  - An `IdSearchResult` — returned as-is from `searchIds()`
  - A flat array of ID strings — converted to `IdSearchResult` automatically by `searchIds()`
  - A `callable(Criteria, Context): mixed` — called with the criteria and context, must return one of the above types
- `$definition` (optional) — An `EntityDefinition` instance, needed if you want realistic primary key handling or entity names in write results.

### Tracking Writes

All write operations are recorded in public arrays for assertion:

- `$repository->creates` — payloads from `create()` calls
- `$repository->updates` — payloads from `update()` calls
- `$repository->upserts` — payloads from `upsert()` calls
- `$repository->deletes` — ID arrays from `delete()` calls

### Adding Search Results Dynamically

Use `addSearch()` to append additional search results after construction:

```php
$repository = new StaticEntityRepository([]);
$repository->addSearch(new EntityCollection([$product]));
$repository->addSearch(fn (Criteria $criteria, Context $context) => new EntityCollection());
```

### Using Callables for Dynamic Results

Pass a callable to inspect the criteria or context and return results conditionally:

```php
$repository = new StaticEntityRepository([
    function (Criteria $criteria, Context $context): EntityCollection {
        // Assert the criteria built by the service under test
        static::assertTrue($criteria->hasFilter('active'));

        return new EntityCollection([$product]);
    },
]);
```

### With EntityDefinition

Pass a definition for proper entity names and primary key resolution in write results:

```php
$repository = new StaticEntityRepository(
    [new EntityCollection([$product])],
    new ProductDefinition()
);
```
