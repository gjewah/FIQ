#coding: utf-8

from odoo import api, fields, models


class knowsystem_tag(models.Model):
    """
    Overwrite to introduce portal security mechanics
    """
    _inherit = "knowsystem.tag"

    @api.depends("partner_ids", "parent_id", "parent_id.all_partner_ids")
    def _compute_all_partner_ids(self):
        """
        Compute method for all_partner_ids
        """
        self.clear_caches() # to avoid taking parent-related cache and sudden error
        left_tag_ids = self
        while left_tag_ids:
            root_tag_ids = left_tag_ids.filtered(lambda fo: fo.parent_id not in left_tag_ids)
            for tag in root_tag_ids:
                this_tag_partner_ids = tag.partner_ids
                parent_tag_id = tag.parent_id
                if parent_tag_id and parent_tag_id.all_partner_ids:
                    this_tag_partner_ids = this_tag_partner_ids | parent_tag_id.all_partner_ids
                tag.all_partner_ids = [(6, 0, this_tag_partner_ids.ids)]
            left_tag_ids -= root_tag_ids

    partner_ids = fields.Many2many(
        "res.partner",
        "res_partner_know_system_tag_rel_table",
        "res_partner_id",
        "knowsystem_tag_id",
        string="Allowed partners",
        help="Portal users of those partners will be able to observe articles with the current tag and its child tags\
disregarding whether an article is published or not",
    )
    all_partner_ids = fields.Many2many(
        "res.partner",
        "res_partner_knowsystem_tag_rel_table",
        "res_partner_id",
        "knowsystem_tag_id",
        string="Access Partners",
        compute=_compute_all_partner_ids,
        compute_sudo=True,
        store=True,
        recursive=True,
    )
