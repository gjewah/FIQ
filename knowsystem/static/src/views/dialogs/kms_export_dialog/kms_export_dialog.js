/** @odoo-module **/

import { ExportDataDialog } from "@web/views/view_dialogs/export_data_dialog";

const defaultArticleFields = ["name", "description", "kanban_manual_description", "section_id", "tag_ids"];


export class KmsExportDataDialog extends ExportDataDialog {
    /*
    * Overwrite to be able to assign default fields
    */
    setDefaultExportList() {
        if (this.state.isCompatible) {
            this.state.exportList = this.state.exportList.filter(
                ({ name }) => this.knownFields[name]
            );
        } else {
            // we use on such approach instead of filtering to save the order of fields and to loop over a short array
            const exportList = [];
            const knownFields = this.knownFields;
            _.each(defaultArticleFields, function(name) {
                exportList.push(knownFields[name]);
            });
            this.state.exportList = exportList;
        }
    }
};
