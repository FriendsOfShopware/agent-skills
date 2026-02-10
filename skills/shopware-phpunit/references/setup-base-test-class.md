---
title: Use the Correct Base Test Class
impact: CRITICAL
impactDescription: Wrong base class causes kernel boot failures or missing database access
tags: setup, kernel, integration, base-class
---

## Use the Correct Base Test Class

Shopware provides different base test classes depending on whether you need the full kernel (integration test) or just isolated logic (unit test). Using the wrong base class leads to missing services, no database access, or unnecessary overhead.

**Incorrect (using raw PHPUnit TestCase for integration tests):**

```php
use PHPUnit\Framework\TestCase;

class MyRepositoryTest extends TestCase
{
    public function testFindProduct(): void
    {
        // This will fail — no kernel, no container, no database
        $repository = $this->getContainer()->get('product.repository');
    }
}
```

**Correct (using Shopware's TestCase for integration tests):**

```php
use Shopware\Core\Framework\Test\TestCaseBase\IntegrationTestBehaviour;
use PHPUnit\Framework\TestCase;

class MyRepositoryTest extends TestCase
{
    use IntegrationTestBehaviour;

    public function testFindProduct(): void
    {
        $repository = static::getContainer()->get('product.repository');

        $context = Context::createDefaultContext();
        $criteria = new Criteria();

        $result = $repository->search($criteria, $context);

        static::assertNotNull($result);
    }
}
```

Use `PHPUnit\Framework\TestCase` (without any Shopware trait) only for pure unit tests that don't need the container or database. Use `IntegrationTestBehaviour` when you need access to services, repositories, or the database.
