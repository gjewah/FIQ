# -*- coding: utf-8 -*-

from odoo import fields, models


class base_document_layout(models.TransientModel):
    """
    Introduced to avoid the error on the core configuration
    """
    _inherit = "base.document.layout"

    external_layout_knowsystem_id = fields.Many2one(related="company_id.external_layout_knowsystem_id", readonly=False)
    knowsystem_custom_layout = fields.Boolean(related="company_id.knowsystem_custom_layout", readonly=False)
