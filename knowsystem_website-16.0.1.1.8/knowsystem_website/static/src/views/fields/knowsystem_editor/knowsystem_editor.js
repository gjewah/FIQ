/** @odoo-module **/

import { KnowSystemEditor } from "@knowsystem/views/fields/knowsystem_editor/knowsystem_editor";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(KnowSystemEditor.prototype, "knowsystem_website_knowsystem_editor_prototype", {
    /*
    * Re-write to add the website service
    */
    setup() {
        this.websiteService = useService("website");
        this._super();
    },
    /*
    * The method to open the website builder for website articles
    */
    async onSwitchEdit() {
        if (this.state.editorType == "website_editor") {
            const saved = await this.props.record.save();
            if (saved) {
                this.websiteService.goToWebsite({
                    path: "/knowsystem/" + this.props.record.data.id, edition: this.state.websiteEditor ? true : false,
                });
            }
        }
        else { this._super() }
    },
})
