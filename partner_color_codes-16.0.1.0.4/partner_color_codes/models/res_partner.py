# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.tools.safe_eval import safe_eval


class res_partner(models.Model):
    """
    Overwritting to add color code/scoring fields
    """
    _inherit = "res.partner"

    def _compute_color_codes_search(self):
        """
        Compute method for color_codes_search (dummy)
        """
        for partner in self:
            partner.color_codes_search = "faotools"

    @api.model
    def search_color_codes_search(self, operator, value):
        """
        Search method for color_code_ids
        Introduced to search also: a) auto rules; b) hierarchically for parents
        """
        partner_ids = []
        color_ids = self.env["color.code"].search([("reference", operator, value)])
        rule_ids = self.env["color.code.rule"].search([
            "|", ("name", operator, value), ("color_code_id", "in", color_ids.ids),
        ])
        for rule in rule_ids:
            partner_ids += self.search(safe_eval(rule_ids.domain)).ids
        code_ids =  self.env["color.code.partner"].search([
            "|", ("name", operator, value), ("color_code_id", "in", color_ids.ids)
        ])
        if code_ids:
            partner_ids += code_ids.mapped("partner_id.id")
        return [("id", "child_of", list(set(partner_ids)))]

    color_code_ids = fields.One2many("color.code.partner", "partner_id", string="Color Codes")
    color_codes_search = fields.Char(
        string="Color Codes Search",
        compute=_compute_color_codes_search,
        compute_sudo=True,
        search="search_color_codes_search"
    )

    def write(self, values):
        """
        Overwrite to manage color codes without checking security rights
        """
        if not values:
            res = super(res_partner, self).write(values)
        elif values.get("color_code_ids"):
            sp_values = {"color_code_ids": values.get("color_code_ids")}
            res = super(res_partner, self.sudo()).write(sp_values)
            values.pop("color_code_ids")
        if values:
            res = super(res_partner, self).write(values)
        return res

    def action_return_colors(self):
        """
        The method to get color codes only
        This is simplified method in comparison to action_return_color_codes to optimize loading without details

        Args:
         * color - char

        Methods:
         * _get_auto_rules

        Returns:
         * list of chars
        """
        parent_id = self.sudo()
        code_ids = self.env["color.code"]
        while parent_id:
            if parent_id.color_code_ids:
                code_ids = code_ids | parent_id.color_code_ids.mapped("color_code_id")
            color_code_rule_ids = parent_id._get_auto_rules()
            if color_code_rule_ids:
                code_ids = code_ids | color_code_rule_ids.mapped("color_code_id")
            parent_id = parent_id.parent_id
        color_codes = code_ids.sorted(lambda code: (code.sequence, code.name)).mapped("name")
        return color_codes

    def action_return_color_codes(self, color=False):
        """
        The method to get all color codes with all properties that relate to the current partner

        Args:
         * color - char

        Methods:
         * _prepare_manual_codes
         * _prepare_auto_codes

        Returns:
         * list of lists of dicts

        Extra info:
         * Expected singleton
        """
        parent_id = self.sudo()
        color_codes = self._prepare_manual_codes(color) + self._prepare_auto_codes(color)
        color_codes = sorted(color_codes, key=lambda code: (code.get("sequence"), code.get("color")))
        return color_codes

    def _prepare_manual_codes(self, color=False):
        """
        The method to prepare manual color codes by this parent and its parents recursively
    
        Args:
         * color

        Returns:
         * list of dicts

        Methods:
         * _get_values of color.code
         * _prepare_manual_codes (recursion)

        Extra_info:
         * Expected singleton
        """
        color_codes = []
        for partner_code in self.color_code_ids:
            if color and partner_code.color_code_id.name != color:
                continue
            code_values = partner_code.color_code_id._get_values()
            code_values.update({
                "id": partner_code.id,
                "name": partner_code.name,
                "code_title":_("By {} on {} for {}".format(
                    partner_code.user_id.name, partner_code.comment_datetime.date(), self.name)
                ),
            })
            color_codes.append(code_values)
        if self.parent_id:
            color_codes += self.parent_id._prepare_manual_codes(color)
        return color_codes

    def _prepare_auto_codes(self, color=False, rules=[]):
        """
        The method to prepare auto color codes by this parent and its parents recursively

        Args:
         * color - char
         * rules - list of ints (rules that have been already considered previously in the recursion)
    
        Methods:
         * _get_auto_rules
         * _get_values of color.code
         * _prepare_auto_codes (recursion)

        Returns:
         * list of dicts

        Extra_info:
         * Expected singleton
        """
        color_codes = []
        color_code_rule_ids = self._get_auto_rules(color, rules)
        for rule in color_code_rule_ids:
            code_values =  rule.color_code_id._get_values()
            code_values.update({
                "id": rule.id, "name": rule.name, "code_title": _("Automatic rule {}".format(rule.name)),
            })
            color_codes.append(code_values)
        new_rules = rules + color_code_rule_ids.ids
        if self.parent_id:
            color_codes += self.parent_id._prepare_auto_codes(color, new_rules)
        return color_codes

    def _get_auto_rules(self, color=False, rules=[]):
        """
        The method to calculate rules applicable to the current partner

        Args:
         * color - False
         * rules - list of ints

        Retunrs:
         * color.code.rule recordset

        Extra info:
         * Expected singleton
        """
        rule_ids = self.env["color.code.rule"]
        if not self or not isinstance(self.id, int):
            return rule_ids
        rule_domain = [("color_code_id", "!=", False), ("id", "not in", rules)]
        if color:
            rule_domain.append(("color_code_id.name", "=", color))
        rules = self.env["color.code.rule"].search(rule_domain)
        base_domain = [("id", "=", self.id)]
        for rule in rules:
            if self.env["res.partner"].search_count(base_domain + safe_eval(rule.domain), limit=1):
                rule_ids += rule
        return rule_ids
