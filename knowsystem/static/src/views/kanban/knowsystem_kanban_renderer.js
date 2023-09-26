/** @odoo-module **/

import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { KnowSystemKanbanRecord } from "./knowsystem_kanban_record";
import { KnowSystemManager } from "@knowsystem/components/knowsystem_manager/knowsystem_manager";
import { KnowSystemNavigation } from "@knowsystem/components/knowsystem_navigation/knowsystem_navigation";


export class KnowSystemKanbanRenderer extends KanbanRenderer {
    /*
    * Prepare props for the KnowSystemManager (right navigation & mass actions component)
    */
    getKnowSystemManagerProps() {
        return {
            currentSelection: this.props.list.selection,
            selection: this.props.list.model.selectedRecords,
            kanbanModel: this.props.list.model,
            canCreate: this.props.archInfo.activeActions.create,
        };
    }
    /*
    * The method to KnowSystemNavigation (left navigation)
    */
    getKnowSystemNavigationProps() {
        const kmsActiveActions = this.props.archInfo.activeActions;
        return {
            kanbanList: this.props.list,
            canCreate: kmsActiveActions.create,
            canDelete: kmsActiveActions.delete,
        }
    }
};

KnowSystemKanbanRenderer.template = "knowsystem.KnowSystemsKanbanRenderer";
KnowSystemKanbanRenderer.components = Object.assign({}, KanbanRenderer.components, {
    KnowSystemManager,
    KnowSystemNavigation,
    KanbanRecord: KnowSystemKanbanRecord,
});
