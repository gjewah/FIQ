/** @odoo-module **/

import { KanbanController } from "@web/views/kanban/kanban_controller";

export class KnowSystemKanbanController extends KanbanController {
    /*
    * The method to launch the template selection wizard and open the new article form
    */
    async createFromTeplate() {
        const { root } = this.model;
        await this.actionService.doAction("knowsystem.create_from_template_action", {additionalContext: root.context});
    }
};

KnowSystemKanbanController.template = "knowsystem.KnowSystemKanbanView";
