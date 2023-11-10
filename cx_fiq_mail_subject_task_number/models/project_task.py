from odoo import models


class ProjectTask(models.Model):
    _inherit = "project.task"

    def _notify_get_recipients_groups(self, msg_vals=None):
        groups = super()._notify_get_recipients_groups(msg_vals)
        for group_data in groups:
            group_data[2].update({"un_reference": self.un_reference})
        return groups

    def _message_create(self, values_list):
        if self.un_reference:
            values_list.update(
                subject="{reference} {task_name}".format(
                    reference=self.un_reference, task_name=values_list["record_name"]
                )
            )
        return super()._message_create(values_list)
