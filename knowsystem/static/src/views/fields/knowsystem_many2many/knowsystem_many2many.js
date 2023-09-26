/** @odoo-module **/

import { registry } from "@web/core/registry";
import { X2ManyField } from "@web/views/fields/x2many/x2many_field";
import { ArticleSearchKanbanRenderer } from "./article_search_kanban_renderer";

export class ArticleSearchMany2many extends X2ManyField { };

ArticleSearchMany2many.components = { ...X2ManyField.components, KanbanRenderer: ArticleSearchKanbanRenderer };

ArticleSearchMany2many.supportedTypes = ["many2many"];
registry.category("fields").add("knowsystem_many2many", ArticleSearchMany2many);


