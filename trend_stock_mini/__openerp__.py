# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Inventory Management [TrendAV]',
    'version': '1.0.1',
    'category': 'Hidden',
    'author': 'Ing. Rigoberto Martínez',
    'maintainer': 'TrendAV',
    'website': 'http://www.trendav.com',
    'sequence': 1,
    'description': """
Inventory, Logistics, Warehousing
=================================
""",
    'depends': ['trend_base','stock'],
    'data': [
             'data/payment_term_data.xml',
             'views/stock_menu.xml',
             "views/stock_view.xml",
    ],
    'demo': [
    ],
    'test': [
    ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
