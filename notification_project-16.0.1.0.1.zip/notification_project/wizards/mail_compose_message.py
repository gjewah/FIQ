# -*- coding: utf-8 -*-

from odoo import models


class mail_compose_message(models.TransientModel):
    """
    Re-write to add table styles
    """
    _inherit = "mail.compose.message"

    def get_mail_values(self, res_ids):
        """
        Re-write to add table styles
        """
        res = super(mail_compose_message, self).get_mail_values(res_ids)
        if self._context.get("faotools_tasks"):
            for res_id in res_ids:
                mail_values = res[res_id]
                if mail_values.get("body_html"):
                    body = self.env["ir.qweb"]._render(
                        "notification_project.tasks_table_mail_layout",
                        {"body": mail_values["body_html"]},
                        minimal_qcontext=True,
                        raise_if_not_found=False,
                    )
                    if body:
                        mail_values["body_html"] = body
        return res
