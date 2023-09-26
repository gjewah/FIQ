/** @odoo-module **/

import { registerPatch } from "@mail/model/model_core";

registerPatch({
    name: "ActivityMenuView",
    recordMethods: {
        /*
        * The method to open an article for quick creation
        */
        async onClickNewArticles(ev) {
            this.update({ isOpen: false });
            await this.env.services.action.doAction("knowsystem.knowsystem_article_action_form_only");
        },
    },
});
