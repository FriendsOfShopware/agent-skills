---
title: Test Store API Routes with SalesChannelApiTestBehaviour
impact: HIGH
impactDescription: Ensures Store API tests have proper sales channel context and authentication
tags: api, store-api, sales-channel, testing
---

## Test Store API Routes with SalesChannelApiTestBehaviour

Store API routes require a sales channel context. Use the `SalesChannelApiTestBehaviour` trait to get a pre-configured browser that handles authentication and sales channel setup.

**Incorrect (manually constructing HTTP requests without proper context):**

```php
public function testStoreApiRoute(): void
{
    $client = static::createClient();
    $client->request('GET', '/store-api/product');

    // Fails: no sales channel context, no sw-access-key header
    static::assertSame(200, $client->getResponse()->getStatusCode());
}
```

**Correct (using SalesChannelApiTestBehaviour):**

```php
use Shopware\Core\Framework\Test\TestCaseBase\IntegrationTestBehaviour;
use Shopware\Core\Framework\Test\TestCaseBase\SalesChannelApiTestBehaviour;
use PHPUnit\Framework\TestCase;

class ProductRouteTest extends TestCase
{
    use IntegrationTestBehaviour;
    use SalesChannelApiTestBehaviour;

    public function testProductListing(): void
    {
        $browser = $this->createCustomSalesChannelBrowser([
            'id' => Uuid::randomHex(),
        ]);

        $browser->request('POST', '/store-api/product-listing/' . $this->getValidCategoryId());

        $response = json_decode($browser->getResponse()->getContent(), true, 512, \JSON_THROW_ON_ERROR);

        static::assertSame(200, $browser->getResponse()->getStatusCode());
        static::assertArrayHasKey('elements', $response);
    }
}
```

The `SalesChannelApiTestBehaviour` trait creates a temporary sales channel and provides a browser client with the correct `sw-access-key` header.
