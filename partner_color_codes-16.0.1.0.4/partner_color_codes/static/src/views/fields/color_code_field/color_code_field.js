/** @odoo-module **/

import { ColorCodes } from "@partner_color_codes/components/color_codes/color_codes";
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";


export class ColorCodeField extends Component {
    /*
    * The method to prepare props for the component ColorCodes
    */
    colorCodeProps() {
        return {
            hasColorCodes: true,
            partnerId: this.props.record.data.id || 0,
        }
    }
};

ColorCodeField.template = "partner_color_codes.ColorCodeField";
ColorCodeField.components = { ColorCodes };
ColorCodeField.props = { ...standardFieldProps };
ColorCodeField.supportedTypes = ["one2many"];


registry.category("fields").add("colorCodeWidget", ColorCodeField);
