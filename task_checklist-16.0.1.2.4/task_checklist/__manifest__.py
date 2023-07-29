# -*- coding: utf-8 -*-
{
    "name": "Task Check List and Approval Process",
    "version": "16.0.1.2.4",
    "category": "Project",
    "author": "faOtools",
    "website": "https://faotools.com/apps/16.0/task-check-list-and-approval-process-762",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "project"
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/project_task_type.xml",
        "views/project_task.xml",
        "views/check_list.xml",
        "data/data.xml"
    ],
    "assets": {
        "web.assets_backend": [
                "task_checklist/static/src/components/task_checklist/*.js",
                "task_checklist/static/src/components/task_checklist/*.xml",
                "task_checklist/static/src/components/task_checklist/*.scss",
                "task_checklist/static/src/views/**/*.js",
                "task_checklist/static/src/views/**/*.xml"
        ]
},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to make sure required jobs are carefully done on this task stage. Tasks checklists. Subtask checklists. Multi level approval. Project checklists. Task validation. Double approval. Checklist alert. To-do list. Custom checklists",
    "description": """For the full details look at static/description/index.html
* Features * 
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "28.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=74&ticket_version=16.0&url_type_id=3",
}