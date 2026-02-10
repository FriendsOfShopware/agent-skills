---
title: Use StaticSystemConfigService Instead of Mocking SystemConfigService
impact: HIGH
impactDescription: Eliminates brittle config mocks and supports sales channel scoping and prefix lookups out of the box
tags: mock, system-config, static-system-config-service, unit-test
---

## Use StaticSystemConfigService Instead of Mocking SystemConfigService

Shopware provides `StaticSystemConfigService` as an in-memory replacement for `SystemConfigService` in unit tests. It accepts a flat config array, supports `get`/`set`/`setMultiple` with optional sales channel scoping, and handles dot-prefix lookups — all without a database.

**Incorrect (manually mocking SystemConfigService):**

```php
public function testMyService(): void
{
    $configService = $this->createMock(SystemConfigService::class);
    $configService->method('get')
        ->willReturnMap([
            ['MyPlugin.config.enabled', null, true],
            ['MyPlugin.config.apiKey', null, 'secret-123'],
        ]);

    // Breaks when the service calls get() with a sales channel ID
    // or fetches a config prefix — willReturnMap can't handle that
    $service = new MyService($configService);
    $service->doSomething();
}
```

**Correct (using StaticSystemConfigService):**

```php
use Shopware\Core\Test\Stub\SystemConfigService\StaticSystemConfigService;

public function testMyService(): void
{
    $configService = new StaticSystemConfigService([
        'MyPlugin.config.enabled' => true,
        'MyPlugin.config.apiKey' => 'secret-123',
    ]);

    $service = new MyService($configService);
    $service->doSomething();
}
```

### Constructor

Accepts a single `array<string, mixed>` mapping config keys to values:

```php
$configService = new StaticSystemConfigService([
    'MyPlugin.config.enabled' => true,
    'MyPlugin.config.limit' => 50,
]);
```

### Sales Channel Scoped Config

Nest config under a sales channel ID key to scope values per channel. When `get()` is called with a sales channel ID, it looks up that scope first:

```php
$configService = new StaticSystemConfigService([
    'MyPlugin.config.mode' => 'default',
    'salesChannelId-123' => [
        'MyPlugin.config.mode' => 'custom',
    ],
]);

$configService->get('MyPlugin.config.mode');                    // 'default'
$configService->get('MyPlugin.config.mode', 'salesChannelId-123'); // 'custom'
```

### Prefix Lookups

Fetching a config prefix returns all matching keys as a nested array, just like the real service:

```php
$configService = new StaticSystemConfigService([
    'MyPlugin.config.enabled' => true,
    'MyPlugin.config.apiKey' => 'secret-123',
]);

$configService->get('MyPlugin.config');
// Returns: ['enabled' => true, 'apiKey' => 'secret-123']
```

### Writing Config in Tests

Use `set()` and `setMultiple()` to change config during a test, for example to verify that your service reacts to config changes:

```php
$configService = new StaticSystemConfigService([
    'MyPlugin.config.enabled' => false,
]);

$configService->set('MyPlugin.config.enabled', true);
$configService->get('MyPlugin.config.enabled'); // true

$configService->setMultiple([
    'MyPlugin.config.limit' => 100,
    'MyPlugin.config.mode' => 'strict',
], 'salesChannelId-456');
```
