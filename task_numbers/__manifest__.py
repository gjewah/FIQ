# -*- coding: utf-8 -*-
{
    "name": "Task Auto Numbering and Search",
    "version": "16.0.1.0.2",
    "category": "Project",
    "author": "faOtools",
    "website": "https://faotools.com/apps/16.0/task-auto-numbering-and-search-765",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "project"
    ],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/project_task.xml",
        "views/project_project.xml",
        "views/res_config_settings.xml",
        "views/project_task_portal.xml"
    ],
    "assets": {
        "web.assets_backend": [
                "task_numbers/static/src/services/*.js",
                "task_numbers/static/src/components/task_search/*.js",
                "task_numbers/static/src/components/task_search/*.xml",
                "task_numbers/static/src/components/task_search/*.scss"
        ]
},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to quickly access and simply reference tasks by automatic numbers. Project tasks sequence. Project task numbering. Project tasks numbering. Project sequence. Projects sequence. Project numbering. Project tasks indexes. Project task sequence number. Project task index. Unique sequence number for tasks. Project tasks referencing. Project tasks quick search.",
    "description": """For the full details look at static/description/index.html
* Features * 
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "48.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=102&ticket_version=16.0&url_type_id=3",
}