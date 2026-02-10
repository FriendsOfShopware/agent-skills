---
title: Bootstrap the Test Kernel Correctly
impact: CRITICAL
impactDescription: Tests will not run without proper kernel bootstrap
tags: setup, kernel, bootstrap, phpunit-xml
---

## Bootstrap the Test Kernel Correctly

Shopware integration tests require a booted Symfony kernel. The bootstrap file and PHPUnit configuration must be set up correctly, or tests will fail with missing class or container errors.

**Incorrect (missing or wrong bootstrap in phpunit.xml):**

```xml
<phpunit bootstrap="vendor/autoload.php">
    <testsuites>
        <testsuite name="Plugin Tests">
            <directory>tests</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

**Correct (using Shopware's test bootstrap):**

```xml
<phpunit bootstrap="tests/TestBootstrap.php">
    <testsuites>
        <testsuite name="Plugin Tests">
            <directory>tests</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

With a `tests/TestBootstrap.php` that boots the Shopware kernel:

```php
<?php

declare(strict_types=1);

use Shopware\Core\TestBootstrapper;

require __DIR__ . '/../vendor/autoload.php';

(new TestBootstrapper())
    ->setPlatformEmbedded(false)
    ->setForceInstallPlugins(true)
    ->bootstrap();
```

The `TestBootstrapper` handles kernel boot, database setup, and plugin installation for the test environment.
