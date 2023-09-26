# -*- coding: utf-8 -*-

from odoo import api, fields, models

class res_config_settings(models.TransientModel):
    """
    Overwrite to add website-specific settings
    """
    _inherit = "res.config.settings"

    @api.model
    def _default_docu_builder_website_id(self):
        """
        Default method for knowsystem_website_id
        """
        return self.env["website"].search([("company_id", "=", self.env.company.id)], limit=1)

    docu_builder_website_id = fields.Many2one(
        "website",
        string="Documentation Website",
        default=_default_docu_builder_website_id, 
        ondelete="cascade",
    )
    documentation_builder_portal = fields.Boolean(
        related="docu_builder_website_id.documentation_builder_portal",
        readonly=False,
    )
    documentation_builder_public = fields.Boolean(
        related="docu_builder_website_id.documentation_builder_public",
        readonly=False,
    )
    group_documentation_versioning = fields.Boolean(
    	string="Versioning",
        implied_group="documentation_builder.group_documentation_versioning",
        group="base.group_public,base.group_portal,base.group_user"
    )
    docu_default_security_action = fields.Selection(
        related="docu_builder_website_id.docu_default_security_action",
        readonly=False,
    )
    docu_attachments_show = fields.Boolean(
        related="docu_builder_website_id.docu_attachments_show",
        readonly=False,
    )
