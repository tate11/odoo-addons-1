# -*- coding: utf-8 -*-
# Copyright 2017 Giacomo Grasso <giacomo.grasso.82@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Financial Management',
    'version': '10.0.1.0',
    'description': """
            Addding financial planning features to accounting
        """,
    'author': 'Giacomo Grasso - giacomo.grasso.82@gmail.com',
    'maintainer': '',
    'website': '',
    'depends': [
        'account',
        'account_accountant',
        'base',
        ],
    'data': [
        'views/account_account.xml',
        'views/account_bank_statement.xml',
        'views/account_move_line.xml',
        'views/finance_menu.xml',
        'views/financial_forecast.xml',
        'views/financial_forecast_template.xml',
        'views/invoice.xml',
        'views/account_journal.xml',

        'security/ir.model.access.csv',
     ],
    'qweb': [
     ],
    'installable': True,
    'auto_install': False,
}