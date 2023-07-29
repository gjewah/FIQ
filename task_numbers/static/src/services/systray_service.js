/** @odoo-module **/

import { TaskQuickSearch } from "@task_numbers/components/task_search/task_search";
import { registry } from "@web/core/registry";
const systrayRegistry = registry.category("systray");

export const taskQuickSearchService = {
    start() {
        systrayRegistry.add("task_numbers.TaskQuickSearch", { Component: TaskQuickSearch }, { sequence: 50 });
    },
};

registry.category("services").add("taskQuickSearchService", taskQuickSearchService);
