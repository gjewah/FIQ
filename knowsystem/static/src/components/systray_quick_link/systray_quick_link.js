/** @odoo-module **/

import { _t } from "web.core";
import { ActionMenus } from "@web/search/action_menus/action_menus";
import { KnowSystemFormViewDialog } from "@knowsystem/views/dialogs/knowsystem_dialog/knowsystem_dialog";
import { patch } from "web.utils";
import { useService } from "@web/core/utils/hooks";

const { Component, onWillStart } = owl;

export class SystrayQuickLink extends Component {
    /*
    * Overwrite to calculate whether KnowSystem is available for quick search
    */
    setup() {
        this.dialogService = useService("dialog");
        this.orm = useService("orm");
        this.router = useService("router");
        this.userService = useService("user");
        onWillStart(async () => {
            this.knowsystemTurn = await this.orm.call("knowsystem.article", "action_check_option", ["knowsystem_systray_option"]);
        });
    }
    /*
    * The method to launch the articles search wizard
    */
    async _onKMSSearch() {
        var kmsModel = false;
        var kmsResIds = [];
        if (this.router.current && this.router.current.hash) {
            kmsModel = this.router.current.hash.model || false;
            kmsResIds = this.router.current.hash.id ? [this.router.current.hash.id] : [];
        }
        const editorRights = await this.userService.hasGroup("knowsystem.group_knowsystem_editor");
        this.dialogService.add(KnowSystemFormViewDialog, {
            resModel: "article.search",
            title: _t("Knowledge Base"),
            context: {
                "kms_model": kmsModel,
                "kms_res_ids": kmsResIds,
                "default_no_selection": true,
                "editorRights": editorRights,
            },
            preventCreate: true,
            onRecordSaved: async (formRecord, params) => {},
            onUnmount: () => { },
        });
    }
}

SystrayQuickLink.template = "knowsystem.SystrayQuickLink";
