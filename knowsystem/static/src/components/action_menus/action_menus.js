/** @odoo-module **/

import { _t } from "web.core";
import { ActionMenus } from "@web/search/action_menus/action_menus";
import { KnowSystemFormViewDialog } from "@knowsystem/views/dialogs/knowsystem_dialog/knowsystem_dialog";
import { patch } from "web.utils";
import { useService } from "@web/core/utils/hooks";

const { onWillStart } = owl;


patch(ActionMenus.prototype, "knowsystem/static/src/components/action_menus.js", {
    /*
    * Overwrite to calculate whether KnowSystem is available for quick search
    */
    setup() {
        this._super(...arguments);
        this.dialogService = useService("dialog");
        this.userService = useService("user");
        onWillStart(async () => {
            this.knowsystemTurn = await this.orm.call("knowsystem.article", "action_check_option", ["knowsystem_models_option"]);
        });
    },
    /*
    * The method to launch the articles search wizard
    */
    async _onKMSSearch() {
        const editorRights = await this.userService.hasGroup("knowsystem.group_knowsystem_editor");
        this.dialogService.add(KnowSystemFormViewDialog, {
            resModel: "article.search",
            title: _t("Knowledge Base"),
            context: {
                "kms_model": this.props.resModel,
                "kms_res_ids": this.props.getActiveIds(),
                "default_no_selection": true,
                "editorRights": editorRights,
            },
            preventCreate: true,
            onRecordSaved: async (formRecord, params) => {},
            onUnmount: () => { },
        });
    },
});
