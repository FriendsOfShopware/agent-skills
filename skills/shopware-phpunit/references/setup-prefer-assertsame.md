---
title: Use assertSame Instead of assertEquals
impact: HIGH
impactDescription: Catches type coercion bugs that assertEquals silently ignores
tags: assertions, assertSame, assertEquals, strict-comparison
---

## Use assertSame Instead of assertEquals

`assertEquals` uses loose comparison (`==`), which silently passes when types differ. `assertSame` uses strict comparison (`===`), catching type mismatches that are often real bugs.

**Incorrect (using assertEquals):**

```php
public function testOrderTotal(): void
{
    $total = $this->orderService->calculateTotal($orderId);

    // Passes even if $total is the string "100" instead of int 100
    static::assertEquals(100, $total);

    // Passes even if getState() returns null instead of ""
    static::assertEquals('', $order->getState());
}
```

**Correct (using assertSame):**

```php
public function testOrderTotal(): void
{
    $total = $this->orderService->calculateTotal($orderId);

    // Fails if $total is not exactly int 100
    static::assertSame(100, $total);

    // Fails if getState() returns null instead of ""
    static::assertSame('', $order->getState());
}
```

Use `assertEquals` only when you intentionally want loose comparison, e.g. comparing `DateTime` objects or objects implementing `__toString`. In all other cases, default to `assertSame`.
