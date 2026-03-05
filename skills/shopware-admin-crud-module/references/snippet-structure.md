---
title: Snippet Structure and Filters
impact: MEDIUM
impactDescription: Missing snippets cause raw translation keys to appear in the UI
tags: snippet, i18n, translation, filter
---

## Snippet Structure

Both `en-GB.json` and `de-DE.json` follow this structure:

```json
{
    "<module-name>": {
        "general": {
            "title": "...",
            "description": "...",
            "placeholderSearchBar": "Search..."
        },
        "list": {
            "title": "...",
            "buttonAdd": "...",
            "columnXxx": "...",
            "textDeleteConfirm": "Are you sure you want to delete \"{name}\"?",
            "titleDeleteConfirm": "Delete ...",
            "messageEmpty": "No items yet",
            "titleSidebarRefresh": "Refresh",
            "filter": {
                "<filter-key>": {
                    "label": "...",
                    "placeholder": "..."
                }
            }
        },
        "detail": {
            "title": "New ...",
            "titleEdit": "...",
            "labelXxx": "...",
            "messageSaveSuccess": "... saved successfully.",
            "messageSaveError": "Could not save ..."
        }
    },
    "global": {
        "entities": {
            "<entity>": "Singular | Plural"
        }
    },
    "sw-privileges": {
        "additional_permissions": {
            "<acl_key>": {
                "label": "... (Frosh Tools)",
                "viewer": "View",
                "editor": "Edit",
                "creator": "Create",
                "deleter": "Delete"
            }
        }
    }
}
```

## Filter Setup

Filters are auto-detected by `filterFactory` from the entity schema:
- **Boolean field** (`active`) -> renders as `sw-boolean-filter` (active/inactive dropdown)
- **ManyToOne/ManyToMany association** (`app`) -> renders as `sw-multi-select-filter` (entity multi-select)

No explicit `type` needed -- just set `property` to the field/association name. Add read privileges for filtered association entities to ACL viewer role.
