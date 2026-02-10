---
title: Use ProductBuilder for Readable Test Data Creation
impact: HIGH
impactDescription: Replaces verbose nested arrays with a fluent builder, cutting product fixture code by 50-80%
tags: data, fixtures, product, builder, integration-test
---

## Use ProductBuilder for Readable Test Data Creation

Shopware ships a `ProductBuilder` that uses a fluent API to construct product data arrays for tests. It handles required fields (tax, product number, stock), manages IDs via `IdsCollection`, and can write directly to the database. This replaces large, error-prone nested arrays.

**Incorrect (manually building product arrays):**

```php
public function testProductListing(): void
{
    $productId = Uuid::randomHex();
    $taxId = Uuid::randomHex();
    $manufacturerId = Uuid::randomHex();

    $repository = static::getContainer()->get('product.repository');
    $repository->create([
        [
            'id' => $productId,
            'name' => 'Test Product',
            'productNumber' => 'SW10001',
            'stock' => 10,
            'active' => true,
            'tax' => [
                'id' => $taxId,
                'name' => 'Standard',
                'taxRate' => 19,
            ],
            'manufacturer' => [
                'id' => $manufacturerId,
                'name' => 'Test Manufacturer',
            ],
            'price' => [
                [
                    'currencyId' => Defaults::CURRENCY,
                    'gross' => 100,
                    'net' => 84.03,
                    'linked' => false,
                ],
            ],
            'visibilities' => [
                [
                    'salesChannelId' => TestDefaults::SALES_CHANNEL,
                    'visibility' => ProductVisibilityDefinition::VISIBILITY_ALL,
                ],
            ],
            'categories' => [
                ['id' => Uuid::randomHex(), 'name' => 'Test Category'],
            ],
        ],
    ], Context::createDefaultContext());
}
```

**Correct (using ProductBuilder):**

```php
use Shopware\Core\Content\Test\Product\ProductBuilder;
use Shopware\Core\Test\Stub\Framework\IdsCollection;

public function testProductListing(): void
{
    $ids = new IdsCollection();

    $product = (new ProductBuilder($ids, 'p1'))
        ->price(100)
        ->manufacturer('m1')
        ->visibility()
        ->category('cat1')
        ->build();

    $repository = static::getContainer()->get('product.repository');
    $repository->create([$product], Context::createDefaultContext());
}
```

### Constructor

```php
new ProductBuilder(IdsCollection $ids, string $productNumber, int $stock = 1, string $taxKey = 't1')
```

- `$ids` — An `IdsCollection` for deterministic, named UUID management
- `$productNumber` — Used as both the product number and the ID key in the IdsCollection
- `$stock` — Initial stock (default: 1)
- `$taxKey` — Key for the auto-created tax entity (default: `'t1'` at 15%)

The builder auto-creates a tax entity and sets the product name to the product number.

### Fluent Methods

#### Core Fields

| Method | Description |
|--------|-------------|
| `name(?string $name)` | Set the product name |
| `active(bool $active)` | Set active state |
| `stock(int $stock)` | Set stock quantity |
| `type(string $type)` | Set product type (physical, digital) |
| `tax(?string $key, int $rate = 15)` | Override tax with a named key and rate |
| `number(string $number)` | Override product number |
| `closeout(?bool $state = true)` | Enable/disable closeout (clearance sale) |
| `releaseDate(string $date)` | Set release date |
| `createdAt(string\|\DateTimeImmutable $date)` | Set created at timestamp |

#### Pricing

| Method | Description |
|--------|-------------|
| `price(float $gross, ?float $net, string $currencyKey = 'default', ?float $listPriceGross, ?float $listPriceNet)` | Set the base price. Net defaults to gross / 1.15 |
| `prices(string $ruleKey, float $gross, string $currencyKey = 'default', ?float $net, int $start = 1, ...)` | Add rule-based advanced prices with quantity ranges |
| `purchasePrice(float $price)` | Set the purchase/cost price |

#### Relations

| Method | Description |
|--------|-------------|
| `manufacturer(string $key, array $translations = [])` | Assign or create a manufacturer |
| `category(string $key)` | Add a category |
| `categories(array $keys)` | Add multiple categories at once |
| `tag(string $key)` | Add a tag |
| `property(string $key, string $group)` | Add a property with its group |
| `visibility(string $salesChannelId = TestDefaults::SALES_CHANNEL, int $visibility = VISIBILITY_ALL)` | Add sales channel visibility |
| `media(string $key, int $position = 0)` | Add a media item |
| `cover(string $key)` | Set cover image |
| `review(string $title, string $content, float $points = 3, ...)` | Add a product review |
| `crossSelling(string $key, string $stream, string $sort = '+name')` | Add a cross-selling with product stream |
| `mainCategory(string $salesChannelId, string $categoryKey)` | Set main category for a sales channel |

#### Variants

| Method | Description |
|--------|-------------|
| `parent(string $key)` | Set parent product (makes this a variant) |
| `variant(array $data)` | Add a child variant |
| `configuratorSetting(string $key, string $group)` | Add a configurator setting (option + group) |
| `option(string $key, string $group, int $position = 1)` | Add a variant option |
| `variantListingConfig(array $data)` | Set variant listing configuration |

#### CMS & SEO

| Method | Description |
|--------|-------------|
| `layout(string $key)` | Assign a CMS layout (creates a default detail page if the key is new) |
| `slot(string $key, array $value, string $languageId = Defaults::LANGUAGE_SYSTEM)` | Configure a CMS slot |
| `seoUrl(string $pathInfo, string $seoPathInfo, ...)` | Add a SEO URL |

#### Other

| Method | Description |
|--------|-------------|
| `customField(string $key, mixed $value)` | Set a custom field value |
| `translation(string $languageId, string $key, mixed $value)` | Add a translation |
| `width/height/length/weight(?float $value)` | Set physical dimensions |

### Writing to Database

Instead of manually calling the repository, use `write()` to persist the product and its dependencies (e.g. custom currencies) in one call:

```php
$ids = new IdsCollection();

(new ProductBuilder($ids, 'p1'))
    ->price(100)
    ->visibility()
    ->write(static::getContainer());
```

### Building Variants

```php
$ids = new IdsCollection();

$parent = (new ProductBuilder($ids, 'parent'))
    ->price(100)
    ->configuratorSetting('red', 'color')
    ->configuratorSetting('xl', 'size')
    ->variant(
        (new ProductBuilder($ids, 'variant-1'))
            ->option('red', 'color')
            ->option('xl', 'size')
            ->stock(5)
            ->build()
    )
    ->build();
```

### Accessing Generated IDs

Since all IDs are managed through `IdsCollection`, you can reference them after building:

```php
$ids = new IdsCollection();
$product = (new ProductBuilder($ids, 'p1'))->price(100)->manufacturer('m1')->build();

$productId = $ids->get('p1');
$manufacturerId = $ids->get('m1');
$taxId = $ids->get('t1');
```
