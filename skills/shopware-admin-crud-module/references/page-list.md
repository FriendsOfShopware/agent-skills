---
title: List Page
impact: CRITICAL
impactDescription: The list page is the main entry point for viewing and managing entities
tags: page, list, listing, grid, inline-edit, delete
---

## List Page

The list page uses the `listing` mixin for pagination, sorting, and search. It includes filters, inline editing, and delete confirmation.

**JS Pattern (`page/<module-name>-list/index.js`):**

```js
import template from './template.html.twig';

const { Mixin } = Shopware;
const { Criteria } = Shopware.Data;

export default {
    template,

    inject: ['repositoryFactory', 'acl', 'filterFactory'],

    mixins: [
        Mixin.getByName('listing'),
        Mixin.getByName('notification'),
    ],

    data() {
        return {
            items: null,
            sortBy: 'name',
            sortDirection: 'ASC',
            isLoading: false,
            showDeleteModal: false,
            filterCriteria: [],
            defaultFilters: [
                // filter keys matching listFilterOptions
            ],
            storeKey: 'grid.filter.<module-name>',
            activeFilterNumber: 0,
        };
    },

    computed: {
        repository() {
            return this.repositoryFactory.create('<entity>');
        },

        listFilterOptions() {
            return {
                // Boolean filter -- auto-detected by filterFactory from entity schema:
                // 'active-filter': {
                //     property: 'active',
                //     label: this.$tc('<module-name>.list.filter.active.label'),
                //     placeholder: this.$tc('<module-name>.list.filter.active.placeholder'),
                // },
                // Entity association filter -- auto-detected as multi-select:
                // 'related-filter': {
                //     property: 'association',
                //     label: this.$tc('<module-name>.list.filter.related.label'),
                //     placeholder: this.$tc('<module-name>.list.filter.related.placeholder'),
                // },
            };
        },

        listFilters() {
            return this.filterFactory.create('<entity>', this.listFilterOptions);
        },
    },

    methods: {
        getList() {
            const criteria = new Criteria(this.page, this.limit);
            this.isLoading = true;

            criteria.setTerm(this.term);
            criteria.addSorting(Criteria.sort(this.sortBy, this.sortDirection));

            this.filterCriteria.forEach((filter) => {
                criteria.addFilter(filter);
            });

            this.activeFilterNumber = this.filterCriteria.length;

            return this.repository.search(criteria).then((result) => {
                this.total = result.total;
                this.items = result;
                this.isLoading = false;
            }).catch(() => {
                this.isLoading = false;
            });
        },

        onInlineEditSave(promise) {
            promise.then(() => {
                this.createNotificationSuccess({
                    message: this.$tc('<module-name>.detail.messageSaveSuccess'),
                });
            }).catch(() => {
                this.getList();
                this.createNotificationError({
                    message: this.$tc('<module-name>.detail.messageSaveError'),
                });
            });
        },

        onDelete(id) {
            this.showDeleteModal = id;
        },

        onCloseDeleteModal() {
            this.showDeleteModal = false;
        },

        onConfirmDelete(id) {
            this.showDeleteModal = false;
            return this.repository.delete(id).then(() => {
                this.getList();
            });
        },

        getColumns() {
            return [
                {
                    property: 'name',
                    label: '<module-name>.list.columnName',
                    routerLink: '<route-prefix>.detail',
                    inlineEdit: 'string',
                    primary: true,
                },
                // Add more columns...
            ];
        },
    },
};
```

**Key patterns:**
- `listing` mixin provides: `page`, `limit`, `term`, `total`, `onSearch`, `onSortColumn`, `onPageChange`, `updateCriteria`
- `getList()` is the canonical method called by the listing mixin
- Delete is two-step: `showDeleteModal = id` then `onConfirmDelete(id)`
- Column `inlineEdit` types: `'string'`, `'number'`, `'boolean'`

**Template Pattern (`page/<module-name>-list/template.html.twig`):**

```html
<sw-page class="<module-name>-list">
    <template #search-bar>
        <sw-search-bar
            initial-search-type="<entity>"
            :initial-search="term"
            @search="onSearch"
        />
    </template>

    <template #smart-bar-header>
        <h2>
            {{ $tc('<module-name>.list.title') }}
            <span v-if="!isLoading" class="sw-page__smart-bar-amount">({{ total }})</span>
        </h2>
    </template>

    <template #smart-bar-actions>
        <mt-button
            v-tooltip.bottom="{
                message: $tc('sw-privileges.tooltip.warning'),
                disabled: acl.can('<acl_key>.creator'),
                showOnDisabledElements: true,
            }"
            :disabled="!acl.can('<acl_key>.creator') || undefined"
            variant="primary"
            @click="$router.push({ name: '<route-prefix>.create' })"
        >
            {{ $tc('<module-name>.list.buttonAdd') }}
        </mt-button>
    </template>

    <template #sidebar>
        <sw-sidebar>
            <sw-sidebar-item
                icon="regular-undo"
                :title="$tc('<module-name>.list.titleSidebarRefresh')"
                @click="getList"
            />
            <sw-sidebar-filter-panel
                entity="<entity>"
                :store-key="storeKey"
                :filters="listFilters"
                :defaults="defaultFilters"
                :active-filter-number="activeFilterNumber"
                @criteria-changed="updateCriteria"
            />
        </sw-sidebar>
    </template>

    <template #content>
        <sw-card-view>
            <mt-empty-state
                v-if="!isLoading && (!items || items.length === 0)"
                :icon="$route.meta.$module.icon"
                :headline="$tc('<module-name>.list.messageEmpty')"
            >
                <template #actions>
                    <mt-button
                        v-if="acl.can('<acl_key>.creator')"
                        variant="primary"
                        @click="$router.push({ name: '<route-prefix>.create' })"
                    >
                        {{ $tc('<module-name>.list.buttonAdd') }}
                    </mt-button>
                </template>
            </mt-empty-state>

            <mt-card v-else :is-loading="isLoading" position-identifier="<module-name>-list">
                <template #grid>
                    <sw-entity-listing
                        detail-route="<route-prefix>.detail"
                        :data-source="items"
                        :columns="getColumns()"
                        :repository="repository"
                        :full-page="false"
                        :show-selection="false"
                        :allow-view="acl.can('<acl_key>.viewer')"
                        :allow-edit="acl.can('<acl_key>.editor')"
                        :allow-inline-edit="acl.can('<acl_key>.editor')"
                        :allow-delete="acl.can('<acl_key>.deleter')"
                        :disable-data-fetching="true"
                        :sort-by="sortBy"
                        :sort-direction="sortDirection"
                        :is-loading="isLoading"
                        @inline-edit-save="onInlineEditSave"
                        @column-sort="onSortColumn"
                        @page-change="onPageChange"
                    >
                        <!-- Custom column slots for non-text fields -->
                        <template #column-active="{ item }">
                            <sw-icon v-if="item.active" name="regular-checkmark-xs" small color="#37d046" />
                            <sw-icon v-else name="regular-times-s" small color="#de294c" />
                        </template>

                        <template #actions="{ item }">
                            <sw-context-menu-item
                                :disabled="!acl.can('<acl_key>.editor')"
                                :router-link="{ name: '<route-prefix>.detail', params: { id: item.id } }"
                            >
                                {{ $tc('global.default.edit') }}
                            </sw-context-menu-item>
                            <sw-context-menu-item
                                variant="danger"
                                :disabled="!acl.can('<acl_key>.deleter')"
                                @click="onDelete(item.id)"
                            >
                                {{ $tc('global.default.delete') }}
                            </sw-context-menu-item>
                        </template>

                        <template #action-modals="{ item }">
                            <sw-modal
                                v-if="showDeleteModal === item.id"
                                :title="$tc('<module-name>.list.titleDeleteConfirm')"
                                @modal-close="onCloseDeleteModal"
                            >
                                <p>{{ $tc('<module-name>.list.textDeleteConfirm', 0, { name: item.name }) }}</p>
                                <template #modal-footer>
                                    <mt-button @click="onCloseDeleteModal">{{ $tc('global.default.cancel') }}</mt-button>
                                    <mt-button variant="critical" @click="onConfirmDelete(item.id)">{{ $tc('global.default.delete') }}</mt-button>
                                </template>
                            </sw-modal>
                        </template>
                    </sw-entity-listing>
                </template>
            </mt-card>
        </sw-card-view>
    </template>
</sw-page>
```

**Critical props on `sw-entity-listing`:**
- `:full-page="false"` -- REQUIRED, otherwise grid uses `position: absolute` and becomes invisible inside `mt-card`
- `:show-selection="false"` -- hides bulk selection checkboxes
- `:disable-data-fetching="true"` -- we control fetching via `getList()`
