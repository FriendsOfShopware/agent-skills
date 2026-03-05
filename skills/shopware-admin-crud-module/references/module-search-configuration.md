---
title: Default Search Configuration
impact: HIGH
impactDescription: Missing search configuration prevents the entity from appearing in global search results
tags: module, search, ranking
---

## Default Search Configuration

The `default-search-configuration.js` defines which fields are searchable and their ranking scores.

**Pattern (`default-search-configuration.js`):**

```js
const defaultSearchConfiguration = {
    _searchable: true,
    // Add searchable string fields from the entity:
    name: {
        _searchable: true,
        _score: 500,    // HIGH
    },
    // _score values: 500 = HIGH, 250 = MIDDLE, 80 = LOW
};

export default defaultSearchConfiguration;
```

Only include string fields that make sense for searching. Skip booleans, integers, FKs, and associations.
