/** @odoo-module **/

import { _t } from "web.core";
import { KnowSystemDialogWrapper } from "@knowsystem/views/dialogs/knowsystem_dialog/knowsystem_dialog";
import { ComponentWrapper } from "web.OwlCompatibility";
import { parseHTML, preserveCursor } from "@web_editor/js/editor/odoo-editor/src/OdooEditor";
import  Wysiwyg from "web_editor.wysiwyg";


Wysiwyg.include({
    /*
     * Re-write to add KnowSystem command if required
    */  
    _getPowerboxOptions: function () {
        const { commands, categories } = this._super.apply(this, arguments);
        if (this.options.KMSTurnOn) {
            commands.push({
                category: _t("Basic blocks"),
                name: _t("KnowSystem"),
                priority: 300,
                description: _t("Knowledge Base"),
                fontawesome: "fa-superpowers",
                callback: () => { this.onOpenKMSDialog() },                
            })
        }
        return { commands, categories };
    },
    /* 
     * The method to open knowsystem search dialog and apply referencing
    */
    onOpenKMSDialog: async function() {
        const restoreSelection = preserveCursor(this.odooEditor.document);
        this.KnowSystemDialogWrapper = new ComponentWrapper(this, KnowSystemDialogWrapper, {
            resModel: "article.search",
            title: _t("Knowledge Base"),
            context: {"kms_model": this.options.KMSModel, "kms_res_ids": [this.options.KMSRecordId]},
            pdfAttach: this.options.pdfAttach,
            onRecordSaved: async (formRecord, params) => { 
                const selectedRecords = formRecord.data.selected_article_ids.records;
                if (params && params.kmsAction && selectedRecords.length > 0) {
                    const actionResult = await this._rpc({
                        model: "knowsystem.article", 
                        method: "action_proceed_article_action", 
                        args: [formRecord.data.selected_article_ids.currentIds, params.kmsAction]
                    });
                    restoreSelection();
                    if (params.kmsAction == "attach") {
                        await this.options.KMSField._onAttachmentChange(actionResult);
                    }
                    else {
                        const htmlToParse = parseHTML(actionResult);
                        this.odooEditor.observerUnactive("commitChanges");
                        this.odooEditor.observerUnactive("handleSelectionInTable");
                        await this.odooEditor.execCommand("insert", htmlToParse);
                        this.odooEditor.observerActive("commitChanges");
                        this.odooEditor.observerActive("handleSelectionInTable");
                    }
                };
            },
            onUnmount: () => { restoreSelection() },
        })
        return this.KnowSystemDialogWrapper.mount(document.body);
    }
});

