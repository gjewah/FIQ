# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "FIQ reference number",
    "summary": """This module displays the task_reference field
                   in the project.task form and kanban views.""",
    "version": "16.0.1.0.0",
    "category": "Product",
    "website": "https://cetmix.com",
    "author": "Cetmix",
    "license": "",
    "installable": True,
    "depends": [
        "task_numbers",
    ],
    "data": ["views/project_task.xml"],
}
