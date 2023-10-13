# Copyright 2023 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

{
    "name": "Project Sequence translation",
    "summary": "change lables on sequence_no fields",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Services/Project",
    "website": "https://github.com/OCA/project",
    "author": "FIQ, Cetmix, Odoo Community Association (OCA)",
    "maintainers": ["Aldeigja"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["project_sequence"],
    "data": [
        "views/project_project.xml",
    ],
}
