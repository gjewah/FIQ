# -*- coding: utf-8 -*-
{
    "name": "KnowSystem: Knowledge Base System",
    "version": "16.0.1.3.5",
    "category": "Extra Tools",
    "author": "faOtools",
    "website": "https://faotools.com/apps/16.0/knowsystem-knowledge-base-system-719",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "mail",
        "web_editor",
        "web"
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/report_paperformat.xml",
        "views/res_config_settings.xml",
        "views/ir_attachment.xml",
        "views/knowsystem_section.xml",
        "views/knowsystem_tag.xml",
        "views/knowsystem_tour.xml",
        "views/knowsystem_article_revision.xml",
        "views/knowsystem_article.xml",
        "views/knowsystem_article_template.xml",
        "wizard/create_from_template.xml",
        "reports/article_report_template.xml",
        "reports/article_report.xml",
        "wizard/article_section_update.xml",
        "wizard/article_tags_update.xml",
        "wizard/add_to_tour.xml",
        "wizard/article_search.xml",
        "wizard/article_groups_update.xml",
        "views/menu.xml",
        "data/cron.xml",
        "data/data.xml",
        "data/mass_actions.xml",
        "views/editor/assets.xml",
        "views/editor/options.xml",
        "views/editor/snippets.xml"
    ],
    "assets": {
        "web.assets_backend": [
                "knowsystem/static/src/models/activity_menu_view/*.js",
                "knowsystem/static/src/components/action_menus/*.xml",
                "knowsystem/static/src/components/action_menus/*.js",
                "knowsystem/static/src/components/knowsystem_manager/*.xml",
                "knowsystem/static/src/components/knowsystem_manager/*.js",
                "knowsystem/static/src/components/knowsystem_jstree_container/*.xml",
                "knowsystem/static/src/components/knowsystem_jstree_container/*.js",
                "knowsystem/static/src/components/knowsystem_learning_tours/*.xml",
                "knowsystem/static/src/components/knowsystem_learning_tours/*.js",
                "knowsystem/static/src/components/knowsystem_navigation/*.xml",
                "knowsystem/static/src/components/knowsystem_navigation/*.js",
                "knowsystem/static/src/components/systray_quick_link/*.xml",
                "knowsystem/static/src/components/systray_quick_link/*.js",
                "knowsystem/static/src/components/activity_menu_view/*.js",
                "knowsystem/static/src/components/activity_menu_view/*.xml",
                "knowsystem/static/src/components/activity_menu_view/*.scss",
                "knowsystem/static/src/views/**/*.xml",
                "knowsystem/static/src/views/**/*.js",
                "knowsystem/static/src/views/**/*.scss",
                "knowsystem/static/src/services/*.js",
                "knowsystem/static/src/knowsystem_editor/knowsystem_for_backend.scss"
        ],
        "web.assets_frontend": [
                "knowsystem/static/src/knowsystem_editor/knowsystem_for_backend.scss"
        ],
        "web.report_assets_common": [
                "knowsystem/static/src/knowsystem_editor/knowsystem_for_backend.scss"
        ],
        "knowsystem.assets_editor": [
                "knowsystem/static/src/knowsystem_editor/knowsystem_editor_snippets_styles.scss"
        ],
        "knowsystem.assets_editor_edition": [
                [
                        "include",
                        "web._assets_helpers"
                ],
                "web/static/src/scss/pre_variables.scss",
                "web/static/lib/bootstrap/scss/_variables.scss"
        ],
        "knowsystem.editor_ui": [
                "knowsystem/static/src/knowsystem_editor/knowsystem_editor_ui.scss"
        ],
        "web_editor.assets_wysiwyg": [
                "knowsystem/static/src/wysiwyg/knowsystem_wysiwyg.js",
                "knowsystem/static/src/wysiwyg/wysiwyg.js",
                "knowsystem/static/src/wysiwyg/snippets_editor.js",
                "knowsystem/static/src/wysiwyg/knowsystem.editor.xml"
        ]
},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to build a deep and structured knowledge base for internal and external use. Knowledge System. KMS. Wiki-like revisions. Knowledge management solution. Notion features. Docket features. Helpdesk knowledge. Collaborative library. Knowledge-based. Internal wiki. Documentation online. Knowledge online.",
    "description": """For the full details look at static/description/index.html
* Features * 
- Single-view knowledge navigation
- Fast, comfortable, and professional knowledge recording
- Get benefit from your knowledge
- &lt;i class=&#39;fa fa-dedent&#39;&gt;&lt;/i&gt; Website documentation builder
- &lt;i class=&#39;fa fa-globe&#39;&gt;&lt;/i&gt; Partner knowledge base portal and public knowledge system
- Interactive and evolving knowledge base
- &lt;i class=&#39;fa fa-info-circle&#39;&gt;&lt;/i&gt; Design eCommerce FAQ or documentation
- Any business and functional area
- &lt;i class=&#39;fa fa-gears&#39;&gt;&lt;/i&gt; Custom knowledge system attributes
- Secured and shared knowledge
#odootools_proprietary""",
    "images": [
        "static/description/main.png"
    ],
    "price": "298.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=83&ticket_version=16.0&url_type_id=3",
}