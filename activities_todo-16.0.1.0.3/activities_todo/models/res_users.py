# -*- coding: utf-8 -*-

from odoo import models, fields


class res_users(models.Model):
    """
    Re write to add activities to-do settings
    """
    _inherit = "res.users"

    act_type_ids = fields.Many2many(
        "mail.activity.type",
        "mail_activity_type_res_users_rel_table",
        "mail_activity_type_id",
        "res_users_id",
        string="To-Do Activity Types",
        help="If not selected, all activity types will be included in to-do lists",
    )
    only_old_activities = fields.Boolean(
        "No Future Activites in To-do",
        help="If checked, to-do lists will not include activities with a deadline in the Future",
        default=True,
    )

    @property
    def SELF_READABLE_FIELDS(self):
        """
        Overwrite to allow users read their own settings
        """
        return super().SELF_READABLE_FIELDS + ["act_type_ids", "only_old_activities"]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        """
        Overwrite to allow users update their own settings
        """
        return super().SELF_WRITEABLE_FIELDS + ["act_type_ids", "only_old_activities"]
