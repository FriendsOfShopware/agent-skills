---
title: Module Registration
impact: CRITICAL
impactDescription: Incorrect module registration prevents the module from loading in the administration
tags: module, registration, routes, settings
---

## Module Registration

The module `index.js` registers components lazily, sets up the search type, and defines routes with ACL privileges.

**Pattern (`index.js`):**

```js
import './acl';
import defaultSearchConfiguration from './default-search-configuration';

Shopware.Component.register('<module-name>-list', () => import('./page/<module-name>-list'));
Shopware.Component.register('<module-name>-detail', () => import('./page/<module-name>-detail'));

const { Module } = Shopware;

Shopware.Service('searchTypeService').upsertType('<entity>', {
    entityName: '<entity>',
    placeholderSnippet: '<module-name>.general.placeholderSearchBar',
    listingRoute: '<route-prefix>.index',
});

Module.register('<module-name>', {
    type: 'plugin',
    name: '<module-name>.general.title',
    title: '<module-name>.general.title',
    description: '<module-name>.general.description',
    color: '#303A4F',
    icon: 'regular-cog',
    entity: '<entity>',
    defaultSearchConfiguration,

    routes: {
        index: {
            component: '<module-name>-list',
            path: 'index',
            meta: {
                parentPath: 'sw.settings.index.plugins',
                privilege: '<acl_key>.viewer',
            },
        },
        detail: {
            component: '<module-name>-detail',
            path: 'detail/:id',
            meta: {
                parentPath: '<route-prefix>.index',
                privilege: '<acl_key>.viewer',
            },
            props: {
                default(route) {
                    return { <entity>Id: route.params.id };
                },
            },
        },
        create: {
            component: '<module-name>-detail',
            path: 'create',
            meta: {
                parentPath: '<route-prefix>.index',
                privilege: '<acl_key>.creator',
            },
        },
    },

    settingsItem: {
        group: 'plugins',
        to: '<route-prefix>.index',
        icon: 'regular-cog',
        privilege: '<acl_key>.viewer',
    },
});
```

**Naming conventions:**
- Module name: `frosh-tools-<entity>` (hyphenated)
- Route prefix: `frosh.tools.<entity>` (dotted) -- derived from module name by replacing hyphens with dots
- ACL key: `frosh_tools_<entity>` (underscored)
