# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Task reference in the mail subject",
    "summary": """This module adds value of the task_reference field into mail subject """,
    "version": "16.0.1.0.0",
    "category": "Product",
    "website": "https://cetmix.com",
    "author": "Cetmix",
    "license": "",
    "installable": True,
    "depends": [
        "task_numbers",
    ],
    "data": ["views/mail_notification_layout.xml"],
}
