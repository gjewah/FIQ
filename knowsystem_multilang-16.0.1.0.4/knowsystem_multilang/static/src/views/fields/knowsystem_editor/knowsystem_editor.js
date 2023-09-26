/** @odoo-module **/

import { _lt } from "@web/core/l10n/translation";
import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";
import { KnowSystemEditor } from "@knowsystem/views/fields/knowsystem_editor/knowsystem_editor";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";


patch(KnowSystemEditor.prototype, "knowsystem_multi_lang_editor", {
    /*
    * Re-write to introduce our own services and action
    */
    setup() {
        this._super.apply(this, arguments);
        this.dialogService = useService("dialog");
    },
    /*
    * Re-write to load available languages
    */
    async _loadSettings(props) {
        await this._super.apply(this, arguments);
        const availableLanguages = await this.orm.call("res.lang", "get_installed", []);
        Object.assign(this.state, {
            availableLanguages: availableLanguages,
            currentLanguage: this.props.record.data.lang,
            stable: this.props.record.data.stable,
        });
    },
    /*
    * The method to change language to show the value in that
    * Note: in readonly mode those changes will not be saved
    */
    async _onChangeLanguage(event) {
        if (this.state.stable) {
            this.state.currentLanguage = event.currentTarget.value;
            const articleVals = await this.orm.read(
                this.props.record.resModel,
                [this.props.record.data.id],
                ["description_arch", "description"],
                { context:  { lang: this.state.currentLanguage } },
            );
            this._updateRecord({
                lang : this.state.currentLanguage,
                description_arch: articleVals[0].description_arch,
                description: articleVals[0].description,
            });
        };
    },
    /*
    * The method to copy description_arch from a different language by selecting language in the wizard
    */
    async onCopyFromLanguage() {
        if (this.state.stable) {
            this.dialogService.add(FormViewDialog, {
                resModel: "article.copy.language",
                context: { default_article_id: this.props.record.data.id, target_lang: this.props.record.data.lang },
                title: _lt("Copy Translation"),
                onRecordSaved: async (formRecord) => {
                    this._updateRecord({description_arch: formRecord.data.description_arch})
                },
            });
        };
    },
});