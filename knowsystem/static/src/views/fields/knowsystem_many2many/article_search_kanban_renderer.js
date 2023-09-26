/** @odoo-module **/

import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { ArticleSearchKanbanRecord } from "./article_search_kanban_record";

export class ArticleSearchKanbanRenderer extends KanbanRenderer {};

ArticleSearchKanbanRenderer.components = Object.assign({}, KanbanRenderer.components, {
    KanbanRecord: ArticleSearchKanbanRecord,
});
