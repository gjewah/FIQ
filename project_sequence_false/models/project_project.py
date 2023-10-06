# Copyright 2023 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)


from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"


    sequence_code = fields.Char(
        copy=False,
        readonly=False,
    )
    name = fields.Char(
        # We actually require it with the SQL constraint, but it is disabled
        # here to let users create/write projects without name, and let this module
        # add a default name if needed
        required=False,
    )

