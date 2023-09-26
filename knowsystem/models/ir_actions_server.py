# -*- coding: utf-8 -*-

from odoo import fields, models


class ir_actions_server(models.Model):
    """
    Overwrite to make it possible to run certain actions under the readonly internal user
    """
    _inherit = "ir.actions.server"

    safe_kms_action = fields.Boolean(string="Safe KMS Action")

    def run(self):
        """
        Overwrite to check knowsystem.article separately, since internal readonly users can make certain actions
        The idea is that readonly users, for example, can print or mass follow. In that case, the action is executed
        under sudo
        """
        for action in self.sudo():
            if action.model_name == "knowsystem.article" and action.safe_kms_action \
                    and self.env.user.has_group("base.group_user") \
                    and not self.env.user.has_group("knowsystem.group_knowsystem_editor"):
                res = super(ir_actions_server, action.sudo()).run()
            else:
                res = super(ir_actions_server, action).run()
        return res
