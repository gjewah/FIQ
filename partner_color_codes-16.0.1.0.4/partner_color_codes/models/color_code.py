# -*- coding: utf-8 -*-

from odoo import _, fields, models


class color_code(models.Model):
    """
    Introducing the model for manage classifier of color codes
    """
    _name = "color.code"
    _description = "Color Code"

    reference = fields.Char(string="Reference", required=True, translate=True, index=True)
    name = fields.Char(string="Color", required=True)
    notes = fields.Text(string="Notes")
    rule_ids = fields.One2many("color.code.rule", "color_code_id", string="Automatic Rules")
    sequence = fields.Integer(string="Sequence")
    active = fields.Boolean(string="Active", default=True)

    _order = "sequence, name, id"

    _sql_constraints = [("name_uniq", "unique(name)", _("The code should have a unique color"))]

    def name_get(self):
        """
        Overloading the method, to use reference as name
        """
        result = []
        for code in self:
            name = u"{} ({})".format(code.reference, code.name)
            result.append((code.id, name))
        return result

    def _get_values(self):
        """
        The method to prepare the dict of color values

        Returns:
         * dict

        Extra info:
         * Expected singleton
        """
        return {
            "color": self.name,
            "sequence": self.sequence,
            "color_title": "{}\n{}".format(self.reference, self.notes or ""),
        }
