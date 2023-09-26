/** @odoo-module **/

import { ColorCodes } from "@partner_color_codes/components/color_codes/color_codes";
import { Many2OneField } from "@web/views/fields/many2one/many2one_field";
import { patch } from "@web/core/utils/patch";

patch(Many2OneField.prototype, "partner_color_codes", {
    /*
    * Getter for hasColorCodes
    */
    get hasColorCodes() {
        return this.relation == "res.partner" && this.resId ? true : false
    },
    /*
    * Getter for partnerId
    */
    colorCodeProps() {
        return {
            hasColorCodes: this.hasColorCodes,
            partnerId: this.resId || 0,
        }
    },
})

Many2OneField.components = {...Many2OneField.components, ColorCodes }
