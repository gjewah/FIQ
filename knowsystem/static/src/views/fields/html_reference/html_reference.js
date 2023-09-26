/** @odoo-module **/

import { HtmlField } from "@web_editor/js/backend/html_field";
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { onWillStart } = owl;

const knowSystemOptionKeys = {"mail.compose.message": "knowsystem_composer_option", "mail.activity": "knowsystem_activity_option"}


patch(HtmlField.prototype, "knowsystem_composer_html_prototype", {
    /*
    * Re-write to get whether the current HTML model is suitable for KnowSystem
    */
    setup() {
        this._super.apply(this, arguments);
        this.orm = useService("orm");
        this.knowsystemTurn = false;
        onWillStart(async () => { await this._checkKMSSetting(this.props) });
    },
    /*
    * The method to define whether the current HTML model is suitable for KnowSystem
    */
    async _checkKMSSetting(self) {
        const knowSystemOptionKey = knowSystemOptionKeys[this.props.record.resModel];
        if (knowSystemOptionKey) {
            this.knowsystemTurn = await this.orm.call("knowsystem.article", "action_check_option", [knowSystemOptionKey])
        };
    },
    /*
    * Re-write to add the KnowSystem command for the special HTML widget
    */    
    get wysiwygOptions() {
        const options = this._super.apply(this, arguments);
        Object.assign(options, {
            KMSField: this,
            KMSTurnOn: this.knowsystemTurn,
            KMSModel: this.props.record.data.model || this.props.record.data.res_model || false,
            KMSRecordId: this.props.record.data.res_id,
            pdfAttach: this.props.record.resModel == "mail.compose.message",
        })
        return options
    },

});
