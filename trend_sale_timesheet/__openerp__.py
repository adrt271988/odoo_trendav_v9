# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sales Timesheet [TrendAV]',
    'version': '1.0.1',
    'category': 'Hidden',
    'author': 'Ing. Rigoberto Martínez',
    'maintainer': 'TrendAV',
    'website': 'http://www.trendav.com',
    'sequence': 15,
    'depends': ['sale_timesheet'],
    'demo': [
    ],
    'summary': 'Sell based on timesheets',
    'description': """
Allows to sell timesheets in your sales order [TrendAV]
=======================================================
    """,
    'data': [
        "views/product_view.xml",
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}

