# -*- coding: utf-8 -*-

from odoo import fields, models


class documentation_version(models.Model):
    """
    The model to introduce sections versions
    """
    _name = "documentation.version"
    _inherit = ["website.published.mixin"]
    _description = "Version"

    name = fields.Char(string="Title", required=True, translate=True)
    section_ids = fields.Many2many(
        "documentation.section",
        "documentation_version_documentation_section_rel_table",
        "documentation_section_rel_id",
        "documentation_version_rel_id",
        string="Sections",
    )
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(string="Color index", default=10)
    sequence = fields.Integer(string="Sequence", default=0)

    _order = "sequence, id"
