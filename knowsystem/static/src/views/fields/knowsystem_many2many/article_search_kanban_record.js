/** @odoo-module **/

import { KanbanRecord } from "@web/views/kanban/kanban_record";
import { KANBAN_BOX_ATTRIBUTE } from "@web/views/kanban/kanban_arch_parser";
const { xml } = owl;


export class ArticleSearchKanbanRecord extends KanbanRecord {
    /*
    * The method to manage clicks on kanban record > add to selection always
    */
    async onGlobalClick(ev) {
        if (ev.target.closest("a.fa-plus-circle")) {
            await  this.props.record.model.root.update(_.object(["selected_article_ids"], [{
                operation: "ADD_M2M",
                ids: [{"id": this.props.record.data.id}],
            }]));
        }
        else { super.onGlobalClick(ev) }
    }
    /*
    * The method to manage key presses on kanban view
    */
    onKeydown(ev) {
        if (ev.key !== "Enter" && ev.key !== " ") { return }
        ev.preventDefault();
        return this.props.record.onRecordClick(ev, {});
    }
};

ArticleSearchKanbanRecord.template = xml`
    <div
        role="article"
        t-att-class="getRecordClasses()"
        t-on-click.synthetic="onGlobalClick"
        t-on-keydown.synthetic="onKeydown"
        t-ref="root">
        <t t-call="{{ templates['${KANBAN_BOX_ATTRIBUTE}'] }}"/>
    </div>`;
