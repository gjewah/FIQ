/** @odoo-module **/

import { registry } from "@web/core/registry";
import { formView } from "@web/views/form/form_view";
import { KnowSystemFormController } from "./knowsystem_form_controller";


export const KnowSystemFormView = Object.assign({}, formView, {
    Controller: KnowSystemFormController,
    buttonTemplate: "knowsystem.KnowSystemFormViewButtons",
});

registry.category("views").add("knowsystem_form", KnowSystemFormView);
