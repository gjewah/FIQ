# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class project_task(models.Model):
    """
    Override to introduce cron to send notifications by project tasks
    """
    _inherit = "project.task"

    def action_get_task_signup_url(self, user_id=False):
        """
        The methdod to generate an access url for task

        Args:
         * user_id - res.users object

        Methods:
         * _get_signup_url_for_action

        Returns:
         * string

        Extra info:
         * expected singleton
        """
        url_user = False
        if user_id:
            partner_id = user_id.partner_id
            url_user = partner_id.with_context(signup_valid=True)._get_signup_url_for_action(
                view_type="form", model=self._name, res_id=self.id,
            )[partner_id.id]
            url_user = url_user.replace("res_id", "id")
        return url_user

    def action_get_deadline_delay(self):
        """
        The method to calculate activity deadline delay in days

        Returns:
         * int

        Extra info:
         * Expected singleton
        """
        return (fields.Date.today() - self.date_deadline).days

    @api.model
    def action_cron_notify(self):
        """
        The method to notify tasks responsibles about overdue and today tasks

        Methods:
         * _render of template
         * _action_send_mail of mail.compose.message
        """
        stage_ids = self.env["project.task.type"].search([("is_notify", "=", True)])
        task_ids = self.env["project.task"].search([
            ("date_deadline", "<=", fields.Date.today()),
            ("stage_id", "in", stage_ids.ids),
            ("user_ids", "!=", False),
        ])
        user_ids = task_ids.mapped("user_ids")
        for user in user_ids:
            try:
                user_task_ids = task_ids.filtered(lambda task: user in task.user_ids)
                if user_task_ids:
                    self = self.with_context(lang=user.partner_id.lang)
                    body_html = self.env["ir.qweb"]._render(
                        "notification_project.project_task_notification_template",
                        {"task_ids": user_task_ids, "assignee_id": user},
                        minimal_qcontext=True,
                        raise_if_not_found=False,
                    )  
                    composer_values = {
                        "author_id": self.env.user.partner_id.id,
                        "body": body_html,
                        "subject": _("Tasks Daily Reminder"),
                        "email_from": self.env.user.partner_id.email_formatted,
                        "record_name": False,
                        "composition_mode": "mass_mail",
                        "template_id": None,
                        "model": "project.task",
                        "partner_ids": [(6, 0, user.partner_id.ids)],
                    }
                    composer = self.env["mail.compose.message"].create(composer_values)
                    composer.with_context(faotools_tasks=True)._action_send_mail(auto_commit=True)
            except Exception as e:
                _logger.error("Daily reminder is not sent to user {}. Reason: {}".format(user.name, e))
