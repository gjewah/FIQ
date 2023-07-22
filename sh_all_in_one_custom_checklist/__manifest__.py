# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name': 'All in One Custom Checklist',
    'author': 'Softhealer Technologies',
    'website': 'https://www.softhealer.com',
    'support': 'support@softhealer.com',
    'license': 'OPL-1',
    'version': '16.0.2',
    'category': 'Extra Tools',
    'summary': 'All in One Checklist Sale Order Checklist,Purchase Order Checklist,Manufacturing Checklist,Stock Checklist,CRM Checklist,Employee Entry Exit Checklist,Meeting Checklist,Project Checklist,Project Task Checklist,MRP Checklist,Sales Checklist,Bunch Checklist Odoo',
    'description': """The checklist used to give an important list of items, things to be done, or points to be considered, used as a reminder. This module helps to track the work of the checklists, All in one custom checklist module includes, sale order custom checklist, purchase order custom checklist, manufacturing custom checklist, meeting custom checklist, project custom checklist, stock custom checklist, task custom checklist, employee entry-exit custom checklist, CRM leads & opportunity custom checklist. Here you can know the detail of the checklist in percentage. This module helps to divide checklist items into different stages. cheers!""",
    'depends': [
        'sale_management',
        'stock',
        'crm',
        'hr',
        'calendar',
        'mrp',
        'project',
        'purchase',
    ],
    'data': [
        'sh_crm_custom_checklist/security/crm_checklist_security.xml',
        'sh_crm_custom_checklist/security/ir.model.access.csv',
        'sh_crm_custom_checklist/views/sh_crm_custom_checklist_views.xml',
        'sh_crm_custom_checklist/views/sh_crm_custom_checklist_template.xml',
        'sh_crm_custom_checklist/views/crm_lead_views.xml',

        'sh_employee_custom_checklist/security/employee_checklist_security.xml',
        'sh_employee_custom_checklist/security/ir.model.access.csv',
        'sh_employee_custom_checklist/views/sh_employee_entry_custom_checklist_views.xml',
        'sh_employee_custom_checklist/views/sh_employee_exit_custom_checklist_views.xml',
        'sh_employee_custom_checklist/views/sh_employee_entry_custom_checklist_template_views.xml',
        'sh_employee_custom_checklist/views/sh_employee_exit_custom_checklist_template_views.xml',
        'sh_employee_custom_checklist/views/hr_employee_views.xml',

        'sh_meeting_custom_checklist/security/ir.model.access.csv',
        'sh_meeting_custom_checklist/views/sh_meeting_checklist_template_views.xml',
        'sh_meeting_custom_checklist/views/calendar_event_views.xml',

        'sh_mrp_custom_checklist/security/mrp_checklist_security.xml',
        'sh_mrp_custom_checklist/security/ir.model.access.csv',
        'sh_mrp_custom_checklist/views/sh_mrp_custom_checklist_views.xml',
        'sh_mrp_custom_checklist/views/sh_mrp_custom_checklist_template_views.xml',
        'sh_mrp_custom_checklist/views/mrp_production_views.xml',
        'sh_mrp_custom_checklist/report/mrp_product_template.xml',

        'sh_project_custom_checklist/security/project_security.xml',
        'sh_project_custom_checklist/security/ir.model.access.csv',
        'sh_project_custom_checklist/views/sh_project_checklist_views.xml',
        'sh_project_custom_checklist/views/sh_project_checklist_template_views.xml',
        'sh_project_custom_checklist/views/project_views.xml',

        'sh_purchase_custom_checklist/security/purchase_checklist_security.xml',
        'sh_purchase_custom_checklist/security/ir.model.access.csv',
        'sh_purchase_custom_checklist/views/sh_purchase_custom_checklist_views.xml',
        'sh_purchase_custom_checklist/views/sh_purchase_custom_checklist_template_views.xml',
        'sh_purchase_custom_checklist/views/purchase_order_views.xml',
        'sh_purchase_custom_checklist/report/purchase_order_template.xml',

        'sh_sale_custom_checklist/security/sale_checklist_security.xml',
        'sh_sale_custom_checklist/security/ir.model.access.csv',
        'sh_sale_custom_checklist/views/sh_sale_custom_checklist_views.xml',
        'sh_sale_custom_checklist/views/sh_sale_custom_checklist_template_views.xml',
        'sh_sale_custom_checklist/views/sale_order_views.xml',
        'sh_sale_custom_checklist/report/sale_order_template.xml',

        'sh_stock_custom_checklist/security/stock_checklist_security.xml',
        'sh_stock_custom_checklist/security/ir.model.access.csv',
        'sh_stock_custom_checklist/views/sh_stock_custom_checklist_views.xml',
        'sh_stock_custom_checklist/views/sh_stock_custom_checklist_template_views.xml',
        'sh_stock_custom_checklist/views/stock_picking_views.xml',
        'sh_stock_custom_checklist/report/stock_picking_template.xml',

        'sh_task_custom_checklist/security/task_checklist_security.xml',
        'sh_task_custom_checklist/security/ir.model.access.csv',
        'sh_task_custom_checklist/views/sh_task_checklist_template_views.xml',
        'sh_task_custom_checklist/views/sh_task_checklist_views.xml',
        'sh_task_custom_checklist/views/project_task_views.xml',

        'sh_product_template_custom_checklist/security/sh_product_security.xml',
        'sh_product_template_custom_checklist/security/ir.model.access.csv',
        'sh_product_template_custom_checklist/views/sh_product_custom_checklist_template_views.xml',
        'sh_product_template_custom_checklist/views/sh_product_custom_checklist_views.xml',
        'sh_product_template_custom_checklist/views/product_template_views.xml',
    ],
    'images': ['static/description/background.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': '45',
    'currency': 'EUR',
}
