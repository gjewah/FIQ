/** @odoo-module **/

import { NewContentModal, MODULE_STATUS } from "@website/systray_items/new_content";
import { patch } from "web.utils";
const { xml } = owl;

patch(NewContentModal.prototype, "knowsystem_website_new_content", {
    setup() {
        this._super();
        const newArticleElement = {
            moduleName: "knowsystem_website",
            moduleXmlId: "base.module_knowsystem_website",
            status: MODULE_STATUS.INSTALLED,
            icon: xml`<i class="fa fa-superpowers"/>`,
            title: this.env._t("Article"),
        };
        this.state.newContentElements.push(newArticleElement)
        newArticleElement.createNewContent = () => this.onAddContent("knowsystem_website.knowsystem_article_action_new_content_add", true);
    },
});
