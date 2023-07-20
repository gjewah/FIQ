# -*- coding: utf-8 -*-
{
    "name": "Activities To-Do Interface",
    "version": "16.0.1.0.3",
    "category": "Productivity",
    "author": "faOtools",
    "website": "https://faotools.com/apps/16.0/activities-to-do-interface-766",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "mail"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/data.xml",
        "wizard/do_with_feedback.xml",
        "wizard/create_new_activity.xml",
        "views/mail_activity_todo.xml",
        "views/res_users.xml"
    ],
    "assets": {
        "web.assets_backend": [
                "activities_todo/static/src/models/activity_menu_view/*.js",
                "activities_todo/static/src/components/activity_menu_view/*.xml",
                "activities_todo/static/src/components/activity_menu_view/*.scss"
        ]
},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to process activities one-by-one in a single interface. Activities management. Odoo activity management. To Do list. Todo list. Activity monitoring. Activity views. Daily activities. Daily to-do list. Mail activity board. Odoo activities list.",
    "description": """For the full details look at static/description/index.html
* Features * 
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "48.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=98&ticket_version=16.0&url_type_id=3",
}