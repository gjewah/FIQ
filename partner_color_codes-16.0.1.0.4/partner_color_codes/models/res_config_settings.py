# -*- coding: utf-8 -*-

from odoo import models


class res_config_settings(models.TransientModel):
    """
    Overwrite to add action to open color codes
    """
    _inherit = "res.config.settings"

    def action_return_color_codes_action(self):
        """
        The method to color codes classifier

        Extra info:
         * Expected singleton
        """
        action_id = self.sudo().env.ref("partner_color_codes.color_code_action").read()[0]
        return action_id
