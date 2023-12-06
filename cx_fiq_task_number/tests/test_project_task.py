# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from collections import OrderedDict

from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests import tagged

from odoo.addons.project.tests.test_project_sharing import TestProjectSharingCommon


@tagged("post_install", "-at_install")
class TestProjectSharingPortal(TestProjectSharingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        project_share_wizard = cls.env["project.share.wizard"].create(
            {
                "access_mode": "edit",
                "res_model": "project.project",
                "res_id": cls.project_portal.id,
                "partner_ids": [
                    Command.link(cls.partner_portal.id),
                ],
            }
        )
        project_share_wizard.action_send_mail()

        Task = cls.env["project.task"]
        cls.read_protected_fields_task = OrderedDict(
            [(k, v) for k, v in Task._fields.items() if k in Task.SELF_READABLE_FIELDS]
        )
        cls.write_protected_fields_task = OrderedDict(
            [(k, v) for k, v in Task._fields.items() if k in Task.SELF_WRITABLE_FIELDS]
        )
        cls.readonly_protected_fields_task = OrderedDict(
            [
                (k, v)
                for k, v in Task._fields.items()
                if k in Task.SELF_READABLE_FIELDS and k not in Task.SELF_WRITABLE_FIELDS
            ]
        )
        cls.other_fields_task = OrderedDict(
            [
                (k, v)
                for k, v in Task._fields.items()
                if k not in Task.SELF_READABLE_FIELDS
            ]
        )

    def test_read_task_with_portal_user(self):
        self.task_portal.with_user(self.user_portal).read(
            self.read_protected_fields_task
        )
        self.task_portal.with_user(self.user_portal).read(
            self.write_protected_fields_task
        )

        with self.assertRaises(AccessError):
            self.task_portal.with_user(self.user_portal).read(self.other_fields_task)

    def test_write_with_portal_user(self):
        self.task_portal.with_user(self.user_portal).write(
            {"un_reference_short": "dummy", "un_reference": "dummy"}
        )

        for field in self.readonly_protected_fields_task:
            with self.assertRaises(AccessError):
                self.task_portal.with_user(self.user_portal).write({field: "dummy"})

        for field in self.other_fields_task:
            with self.assertRaises(AccessError):
                self.task_portal.with_user(self.user_portal).write({field: "dummy"})
