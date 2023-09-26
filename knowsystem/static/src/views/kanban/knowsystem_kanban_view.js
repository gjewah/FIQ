/** @odoo-module **/

import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { KnowSystemKanbanController } from "./knowsystem_kanban_controller";
import { KnowSystemKanbanModel } from "./knowsystem_kanban_model";
import { KnowSystemKanbanRenderer } from "./knowsystem_kanban_renderer";
import { KnowSystemSearchModel } from "../search/knowsystem_search_model";

export const KnowSystemKanbanView = Object.assign({}, kanbanView, {
    SearchModel: KnowSystemSearchModel,
    Controller: KnowSystemKanbanController,
    Model: KnowSystemKanbanModel,
    Renderer: KnowSystemKanbanRenderer,
    searchMenuTypes: ["filter", "favorite"],
    buttonTemplate: "knowsystem.KnowSystemKanbanViewButtons",
});

registry.category("views").add("knowsystem_kanban", KnowSystemKanbanView);
