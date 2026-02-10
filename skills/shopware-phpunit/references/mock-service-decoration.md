---
title: Mock Services via Container Instead of Constructor Injection
impact: MEDIUM
impactDescription: Avoids brittle mocks and tests that break on refactoring
tags: mock, service, container, dependency-injection
---

## Mock Services via Container Instead of Constructor Injection

In integration tests, replace services in the DI container rather than manually constructing classes with mocked dependencies. This ensures decorators, event listeners, and other wiring still work correctly.

**Incorrect (manually constructing the service with mocks):**

```php
public function testMyService(): void
{
    $repositoryMock = $this->createMock(EntityRepository::class);
    $repositoryMock->method('search')->willReturn(new EntitySearchResult(
        'product', 0, new EntityCollection(), null, new Criteria(), Context::createDefaultContext()
    ));

    // Breaks if MyService constructor changes or has additional dependencies
    $service = new MyService($repositoryMock, $this->createMock(EventDispatcherInterface::class));
    $result = $service->doSomething();

    static::assertTrue($result);
}
```

**Correct (replacing the service in the container):**

```php
use Shopware\Core\Framework\Test\TestCaseBase\IntegrationTestBehaviour;

class MyServiceTest extends TestCase
{
    use IntegrationTestBehaviour;

    public function testMyService(): void
    {
        $mock = $this->createMock(SomeExternalDependency::class);
        $mock->method('call')->willReturn('mocked-value');

        static::getContainer()->set(SomeExternalDependency::class, $mock);

        $service = static::getContainer()->get(MyService::class);
        $result = $service->doSomething();

        static::assertTrue($result);
    }
}
```

Only mock external boundaries (HTTP clients, third-party APIs). For Shopware services and repositories, prefer using the real implementations in integration tests.
