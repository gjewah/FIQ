/** @odoo-module **/

import { _lt } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";
import { Component, onMounted, onRendered, onWillUnmount, xml } from "@odoo/owl";
import { useChildRef } from "@web/core/utils/hooks";
import { useService } from "@web/core/utils/hooks";
import { useWowlService } from '@web/legacy/utils';
import { View } from "@web/views/view";


export class KnowSystemFormViewDialog extends Component {
    setup() {
        super.setup();
        this.actionService = useService("action");
        this.modalRef = useChildRef();
        const buttonTemplate = "knowsystem.KnowSystemFormViewDialog.buttons";
        this.viewProps = {
            type: "form",
            buttonTemplate: buttonTemplate,
            context: this.props.context || {},
            display: { controlPanel: false },
            mode: "edit",
            resId: this.props.resId || false,
            resModel: this.props.resModel,
            viewId: this.props.viewId || false,
            preventCreate: this.props.preventCreate || false,
            preventEdit: false,
            info: { pdfAttach: this.props.pdfAttach },
            discardRecord: () => { this.props.close() },
            saveRecord: async (record, params) => {
                if (params.newOpen) {
                    this.actionService.doAction("knowsystem.knowsystem_article_action_form_only");
                    this.props.close();
                    return
                };
                await this.props.onRecordSaved(record, params);
                this.props.close();
            },
        };
        onMounted(() => {
            // Hide excess buttons
            if (this.modalRef.el.querySelector(".modal-footer").childElementCount > 1) {
                const defaultButton = this.modalRef.el.querySelector(".modal-footer button.o-default-button");
                if (defaultButton) { defaultButton.classList.add("d-none") };
            };
        });
        onWillUnmount(() => { this.props.onUnmount() });
    }
};

KnowSystemFormViewDialog.template = "knowsystem.KnowSystemFormViewDialog";
KnowSystemFormViewDialog.components = { Dialog, View };
KnowSystemFormViewDialog.props = {
    close: Function,
    resModel: String,
    context: { type: Object, optional: true },
    mode: {
        optional: true,
        validate: (m) => ["edit", "readonly"].includes(m),
    },
    onRecordSaved: { type: Function, optional: true },
    onUnmount: { type: Function, optional: true },
    preventCreate: { type: Boolean, optional: true },
    resId: { type: [Number, Boolean], optional: true },
    title: { type: String, optional: true },
    viewId: { type: [Number, Boolean], optional: true },
    size: Dialog.props.size,
    pdfAttach: { type: Boolean, optional: true },
};
KnowSystemFormViewDialog.defaultProps = { onRecordSaved: () => {} };

export class KnowSystemDialogWrapper extends Component {
    setup() {
        this.dialogs = useWowlService("dialog");
        onRendered(() => { this.dialogs.add(KnowSystemFormViewDialog, this.props) });
    }
}
KnowSystemDialogWrapper.template = xml``;


