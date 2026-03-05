---
title: ACL Privilege Mapping
impact: HIGH
impactDescription: Missing ACL setup causes permission errors or unrestricted access to module functionality
tags: acl, privileges, permissions, security
---

## ACL Privilege Mapping

The ACL configuration defines four roles (viewer, editor, creator, deleter) with proper dependency chains.

**Pattern (`acl/index.js`):**

```js
Shopware.Service('privileges').addPrivilegeMappingEntry({
    category: 'additional_permissions',
    parent: null,
    key: '<acl_key>',
    roles: {
        viewer: {
            privileges: [
                '<entity>:read',
                // Add read privileges for any related entities shown in filters/detail
            ],
            dependencies: [],
        },
        editor: {
            privileges: ['<entity>:update'],
            dependencies: ['<acl_key>.viewer'],
        },
        creator: {
            privileges: ['<entity>:create'],
            dependencies: ['<acl_key>.viewer', '<acl_key>.editor'],
        },
        deleter: {
            privileges: ['<entity>:delete'],
            dependencies: ['<acl_key>.viewer'],
        },
    },
});
```

Add read privileges for any related entities that are displayed in filters or detail views to the `viewer` role.
