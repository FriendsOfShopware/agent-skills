---
title: Use expectExceptionObject Instead of expectException and expectExceptionMessage
impact: HIGH
impactDescription: Single call replaces two, and asserts the exact exception instance including class, message, and code
tags: exceptions, assertions, expectExceptionObject, best-practice
---

## Use expectExceptionObject Instead of expectException and expectExceptionMessage

`expectExceptionObject` validates the exception class, message, and code in one call by comparing against an actual exception instance. This is easier to maintain than separate `expectException` + `expectExceptionMessage` calls and ensures the test matches the exact exception the code throws.

**Incorrect (separate expectException and expectExceptionMessage):**

```php
public function testThrowsOnInvalidProduct(): void
{
    // Two separate calls to maintain, message can drift out of sync
    $this->expectException(ProductNotFoundException::class);
    $this->expectExceptionMessage('Product with id "abc" not found');

    $this->productService->get('abc', Context::createDefaultContext());
}
```

**Correct (using expectExceptionObject):**

```php
public function testThrowsOnInvalidProduct(): void
{
    $this->expectExceptionObject(
        new ProductNotFoundException('abc')
    );

    $this->productService->get('abc', Context::createDefaultContext());
}
```

This asserts the exception class, message, and code all at once. When the exception message format changes, you only update the exception class itself — the test stays in sync automatically because it constructs the same exception object.
