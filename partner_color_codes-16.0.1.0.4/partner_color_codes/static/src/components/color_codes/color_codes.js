/** @odoo-module */

import { _lt } from "@web/core/l10n/translation";
import { Domain } from "@web/core/domain";
import { Component, useState, onWillStart, onWillUpdateProps } from "@odoo/owl";
import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";
import { Tooltip } from "@web/core/tooltip/tooltip";
import { useService } from "@web/core/utils/hooks";


export class ColorCodes extends Component {
    /*
    * The method to set up initial values
    */
    setup() {
        this.orm = useService("orm");
        this.dialogService = useService("dialog");
        this.state = useState({ colorCodes: [], fullColors: null, fullColorsShown: false, colors: {} });
        this.popover = useService("popover");
        onWillStart(async () => {
            await this.onGetColorCodes(this.props);
        });
        onWillUpdateProps(async (nextProps) => {
            await this.onGetColorCodes(nextProps);
        });
    }
    /*
    * The method to calculate checkpoints available for the current stage and team
    */
    async onGetColorCodes(props) {
        var colorCodes = [];
        if (props.partnerId) {
            colorCodes = await this.orm.call("res.partner", "action_return_colors", [props.partnerId]);
        };
        Object.assign(this.state, { colorCodes: colorCodes, fullColors: null, colors: {} });
    }
    /*
    * The method to show the dialog with all colors and hints
    */
    async onClickColorBox(event) {
        if (this.props.partnerId) {
            if (!this.state.fullColors) {
                const colorCodes = await this.orm.call(
                    "res.partner", "action_return_color_codes", [this.props.partnerId, false]
                );
                this.state.fullColors = colorCodes;
            };
            this.addPopover(event, this.state.fullColors, true);
            this.fullColorsShown = true;
        };
    }
    /*
    * The method to show a short preview of the current color
    */
    async onShowColorBox(event, color) {
        this.fullColorsShown = false;
        if (this.props.partnerId) {
            if (!this.state.colors[color]) {
                const colorCodes = await this.orm.call(
                    "res.partner", "action_return_color_codes", [this.props.partnerId, color]
                );
                this.state.colors[color] = colorCodes;
            };
            this.addPopover(event, this.state.colors[color], false);
        };
    }
    /*
    * The method to hide a short preview of the current color
    */
    async onHideColorBox(forceClose) {
        if ((!this.fullColorsShown || forceClose) && this.closeTooltip) {
            this.closeTooltip();
        };
    }
    /*
    * The method to add the colors popover
    */
    async addPopover(event, colorCodes, showClose=false) {
        this.onHideColorBox(true);
        this.closeTooltip = this.popover.add(
            $(event.target)[0], 
            Tooltip, 
            {
                template: "partner_color_codes.ColorCodesToolTip",
                info: { colorCodes : colorCodes, close: this.onHideColorBox.bind(this), showClose: showClose },
            },
            { popoverClass: "" },
        );
    }
    /*
    * The method to add manual color codes
    */
    async onEditColorBox() {
        var self = this;
        this.dialogService.add(FormViewDialog, {
            resModel: "res.partner",
            resId: this.props.partnerId,
            title: _lt("Color codes"),
            preventCreate: true,
            preventEdit: false,
            context: { form_view_ref: "partner_color_codes.res_partner_view_form_codes_special" },
            onRecordSaved: async (formRecord) => {
                await self.onGetColorCodes(self.props);
            },
        });

    }
}

ColorCodes.template = "partner_color_codes.ColorCodes";
ColorCodes.props = {
    partnerId: { type: Number },
    hasColorCodes: { type: Boolean, optional: false },
};
