# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': u'中南大学教学模块',
    'version': '2.0',
    'category': u'中南大学',
    'sequence': 30,
    'summary': u'中南大学教学模块说明书',
    'description': """
Manage expenses by Employees
============================

This application allows you to manage your employees' daily expenses. It gives you access to your employees’ fee notes and give you the right to complete and validate or refuse the notes. After validation it creates an invoice for the employee.
Employee can encode their own expenses and the validation flow puts it automatically in the accounting after validation by managers.


The whole flow is implemented as:
---------------------------------
* Draft expense
* Submitted by the employee to his manager
* Approved by his manager
* Validation by the accountant and accounting entries creation

This module also uses analytic accounting and is compatible with the invoice on timesheet module so that you are able to automatically re-invoice your customers' expenses if your work by project.
    """,
    'author': 'Odoo S.A.',
    'website': 'https://www.odoo.com/page/expenses',
    'depends': ['base_setup', 'product', 'analytic', 'report', 'web_tip', 'web_planner','website','website_form'],
    'data': [
        'security/restaurant_security.xml',
        'security/ir.model.access.csv',
        'views/zndx_sequence.xml',
        'views/restaurant_menu.xml',
        'views/restaurant_view.xml',
        'views/soup_view.xml',
        'views/waiter_view.xml',
        'views/order_pay_wizard_view.xml',
        'views/order_view.xml',
        'controller/main_template.xml',
        'controller/submit_order.xml',
        'data/zndx_data.xml',

    ],
    'demo': [
        'demo/account_demo.xml',
    ],
    'qweb': [
        "static/src/xml/account_reconciliation.xml",
        "static/src/xml/account_payment.xml",
        "static/src/xml/account_report_backend.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
