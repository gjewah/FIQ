/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";

const { Component, onWillStart } = owl;


export class TaskQuickSearch extends Component {
    /*
    * Overwrite to calculate whether KnowSystem is available for quick search
    */
    setup() {
        this.actionService = useService("action");
        this.orm = useService("orm");
        this.userService = useService("user");
        onWillStart(async () => {
            this.projectUser = await this.userService.hasGroup("project.group_project_user");
        });
    }
    /*
    * The method to launch the articles search wizard
    */
    async _makeSearch(event) {
        if (event.which === 13) {
            const searchInputObject = $(event.target)[0];
            const actionId = await this.orm.call("project.task", "action_quick_search", [searchInputObject.value])
            searchInputObject.value = "";
            this.actionService.doAction(actionId, { clear_breadcrumbs: true });
        }
    }
}

TaskQuickSearch.template = "task_numbers.QuickSearch";
