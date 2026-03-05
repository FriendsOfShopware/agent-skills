---
title: Detail/Create Page
impact: CRITICAL
impactDescription: The detail page handles both creating new entities and editing existing ones
tags: page, detail, create, form, save
---

## Detail/Create Page

The same component serves both create and detail views, distinguished by the entity ID prop being `null` (create) or a UUID (edit).

**JS Pattern (`page/<module-name>-detail/index.js`):**

```js
import template from './template.html.twig';

const { Mixin } = Shopware;
const { mapPropertyErrors } = Shopware.Component.getComponentHelper();

export default {
    template,

    inject: ['repositoryFactory', 'acl'],

    mixins: [
        Mixin.getByName('notification'),
    ],

    shortcuts: {
        'SYSTEMKEY+S': {
            active() { return this.allowSave; },
            method: 'onSave',
        },
        ESCAPE: 'onCancel',
    },

    props: {
        <entity>Id: {
            type: String,
            required: false,
            default: null,
        },
    },

    data() {
        return {
            entity: null,
            isLoading: false,
            isSaveSuccessful: false,
        };
    },

    computed: {
        repository() {
            return this.repositoryFactory.create('<entity>');
        },

        isNew() {
            return this.entity?.isNew?.() ?? false;
        },

        allowSave() {
            return this.isNew
                ? this.acl.can('<acl_key>.creator')
                : this.acl.can('<acl_key>.editor');
        },

        tooltipSave() {
            if (!this.allowSave) {
                return {
                    message: this.$tc('sw-privileges.tooltip.warning'),
                    showOnDisabledElements: true,
                };
            }
            return { message: `${this.$device.getSystemKey()} + S`, appearance: 'light' };
        },

        // For date formatting in templates:
        // date() {
        //     return Shopware.Filter.getByName('date');
        // },

        ...mapPropertyErrors('<entity>', ['field1', 'field2']),
    },

    watch: {
        <entity>Id() {
            this.createdComponent();
        },
    },

    created() {
        this.createdComponent();
    },

    methods: {
        createdComponent() {
            this.isLoading = true;

            if (this.<entity>Id) {
                this.repository.get(this.<entity>Id).then((result) => {
                    this.entity = result;
                    this.isLoading = false;
                });
            } else {
                this.entity = this.repository.create();
                this.isLoading = false;
            }
        },

        onSave() {
            this.isSaveSuccessful = false;
            this.isLoading = true;

            return this.repository.save(this.entity).then(() => {
                this.isSaveSuccessful = true;

                if (!this.<entity>Id) {
                    this.$router.push({
                        name: '<route-prefix>.detail',
                        params: { id: this.entity.id },
                    });
                }

                return this.repository.get(this.entity.id).then((updated) => {
                    this.entity = updated;
                    this.isLoading = false;
                });
            }).catch(() => {
                this.createNotificationError({
                    message: this.$tc('<module-name>.detail.messageSaveError'),
                });
                this.isLoading = false;
            });
        },

        onCancel() {
            this.$router.push({ name: '<route-prefix>.index' });
        },
    },
};
```

**Key patterns:**
- `repository.create()` for new entities, `repository.get(id)` for existing
- After create save, redirect to detail route with the new ID
- `mapPropertyErrors` maps validation errors from entity store to computed properties for form field `:error` binding

**Template Pattern (`page/<module-name>-detail/template.html.twig`):**

```html
<sw-page class="<module-name>-detail">
    <template #smart-bar-header>
        <h2 v-if="entity && entity.name">{{ entity.name }}</h2>
        <h2 v-else>{{ $tc('<module-name>.detail.title') }}</h2>
    </template>

    <template #smart-bar-actions>
        <mt-button
            v-tooltip.bottom="{ message: 'ESC', appearance: 'light' }"
            :disabled="isLoading"
            variant="secondary"
            @click="onCancel"
        >
            {{ $tc('global.default.cancel') }}
        </mt-button>

        <sw-button-process
            v-model:process-success="isSaveSuccessful"
            v-tooltip.bottom="tooltipSave"
            variant="primary"
            :is-loading="isLoading"
            :disabled="isLoading || !allowSave || undefined"
            @click.prevent="onSave"
        >
            {{ $tc('global.default.save') }}
        </sw-button-process>
    </template>

    <template #content>
        <sw-card-view>
            <template v-if="isLoading">
                <sw-skeleton />
                <sw-skeleton />
            </template>

            <template v-else>
                <mt-card :title="$tc('<module-name>.detail.titleEdit')" position-identifier="<module-name>-detail">
                    <sw-container columns="repeat(auto-fit, minmax(250px, 1fr))" gap="0px 30px">
                        <!-- Text fields use v-model directly -->
                        <mt-text-field
                            v-model="entity.name"
                            :label="$tc('<module-name>.detail.labelName')"
                            :disabled="!allowSave || undefined"
                            :error="entityNameError"
                            required
                        />
                    </sw-container>

                    <!-- Boolean fields use mt-switch with explicit :model-value + @update:model-value -->
                    <sw-container columns="repeat(auto-fit, minmax(250px, 1fr))" gap="0px 30px">
                        <mt-switch
                            :model-value="entity.active"
                            :label="$tc('<module-name>.detail.labelActive')"
                            :disabled="!allowSave || undefined"
                            @update:model-value="entity.active = $event"
                        />
                    </sw-container>
                </mt-card>
            </template>
        </sw-card-view>
    </template>
</sw-page>
```

**Component gotchas:**
- Use `mt-switch` for booleans (NOT `sw-switch-field`) -- use `:model-value` + `@update:model-value`, not `v-model`
- Use `mt-text-field` for text inputs -- `v-model` works here
- Use `mt-number-field` for numbers
- Use `mt-button` for buttons, `sw-button-process` for the save button
- Use `mt-card` (NOT `sw-card`) with required `position-identifier` prop
- ACL disable pattern: `:disabled="!allowSave || undefined"` (the `|| undefined` avoids rendering `disabled="false"`)
- Date formatting: define `date()` computed returning `Shopware.Filter.getByName('date')`, then call `date(value, options)` in template (Vue 3 has no `| filter` syntax)
