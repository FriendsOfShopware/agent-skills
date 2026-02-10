---
title: Create Test Data with IdsCollection for Readable Tests
impact: MEDIUM
impactDescription: Makes tests easier to read and avoids UUID management boilerplate
tags: data, fixtures, ids, uuid
---

## Create Test Data with IdsCollection for Readable Tests

Shopware's `IdsCollection` provides a convenient way to manage UUIDs in tests. Instead of manually generating and tracking random hex strings, use named IDs that make test code self-documenting.

**Incorrect (manual UUID management):**

```php
public function testOrderWorkflow(): void
{
    $productId = Uuid::randomHex();
    $customerId = Uuid::randomHex();
    $orderId = Uuid::randomHex();
    $orderLineItemId = Uuid::randomHex();
    $addressId = Uuid::randomHex();

    // Hard to track which ID belongs to what
    $this->createProduct($productId);
    $this->createCustomer($customerId, $addressId);
    $this->createOrder($orderId, $customerId, $productId, $orderLineItemId, $addressId);

    $result = $this->orderService->process($orderId);
}
```

**Correct (using IdsCollection):**

```php
use Shopware\Core\Framework\Test\IdsCollection;

public function testOrderWorkflow(): void
{
    $ids = new IdsCollection();

    $this->createProduct($ids->get('product'));
    $this->createCustomer($ids->get('customer'), $ids->get('address'));
    $this->createOrder(
        $ids->get('order'),
        $ids->get('customer'),
        $ids->get('product'),
        $ids->get('order-line-item'),
        $ids->get('address'),
    );

    $result = $this->orderService->process($ids->get('order'));
}
```

`IdsCollection::get()` returns the same UUID for the same name within an instance, so you can reference entities by meaningful names instead of raw hex strings.
