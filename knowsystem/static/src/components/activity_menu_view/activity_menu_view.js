/** @odoo-module **/

import "@mail/components/activity_menu_view/activity_menu_view";
import { getMessagingComponent } from "@mail/utils/messaging_component";
import { patch } from "web.utils";
import { useService } from "@web/core/utils/hooks";

const { onWillStart } = owl;
const ActivityMenuView = getMessagingComponent("ActivityMenuView");


patch(ActivityMenuView.prototype, "knowsystem_quick_create", {
    /*
    * Re-write to define whether the quick create option should be shown
    */
    setup() {
        this.orm = useService("orm");
        onWillStart(async () => {
            this.kmsQuickCreate = await this.orm.call("knowsystem.article", "action_check_quick_creation", []);
        });
        this._super();
    },
});
