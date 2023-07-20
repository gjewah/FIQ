/** @odoo-module **/

import { registerPatch } from "@mail/model/model_core";

registerPatch({
    name: "ActivityMenuView",
    recordMethods: {
        /*
        * The method to execute activities to-do action
        */
        async onClickStartToDo(ev) {
            this.update({ isOpen: false });
            const actionId = await this.env.services.orm.call("mail.activity.todo", "action_start_todo", []);
            await this.env.services.action.doAction(actionId);
        },
    },
});
