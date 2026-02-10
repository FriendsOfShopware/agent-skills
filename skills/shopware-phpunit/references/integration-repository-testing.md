---
title: Test Repositories with Proper Context and Cleanup
impact: HIGH
impactDescription: Avoids flaky tests from leftover data or wrong context
tags: integration, repository, context, database, transactions
---

## Test Repositories with Proper Context and Cleanup

When testing Shopware repositories, always use the correct Context, create test data explicitly, and rely on the `IntegrationTestBehaviour` trait's automatic transaction rollback to keep tests isolated.

**Incorrect (relying on existing data, no isolation):**

```php
public function testProductCount(): void
{
    $repository = static::getContainer()->get('product.repository');
    $result = $repository->search(new Criteria(), Context::createDefaultContext());

    // Fragile: depends on whatever data exists in the test database
    static::assertGreaterThan(0, $result->getTotal());
}
```

**Correct (create own test data, use proper context):**

```php
use Shopware\Core\Framework\Test\TestCaseBase\IntegrationTestBehaviour;
use Shopware\Core\Framework\Context;
use Shopware\Core\Framework\DataAbstractionLayer\Search\Criteria;
use Shopware\Core\Framework\Uuid\Uuid;

class ProductRepositoryTest extends TestCase
{
    use IntegrationTestBehaviour;

    public function testProductCanBeCreatedAndFound(): void
    {
        $repository = static::getContainer()->get('product.repository');
        $context = Context::createDefaultContext();
        $id = Uuid::randomHex();

        $repository->create([
            [
                'id' => $id,
                'name' => 'Test Product',
                'productNumber' => Uuid::randomHex(),
                'stock' => 10,
                'tax' => ['name' => 'test', 'taxRate' => 19],
                'price' => [
                    ['currencyId' => Defaults::CURRENCY, 'gross' => 100, 'net' => 84.03, 'linked' => false],
                ],
            ],
        ], $context);

        $result = $repository->search(new Criteria([$id]), $context);

        static::assertCount(1, $result);
        static::assertSame('Test Product', $result->first()->getName());
    }
}
```

The `IntegrationTestBehaviour` trait wraps each test in a database transaction that is rolled back after the test, so created data does not leak between tests.
