# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Point of Sale [Mimoki]',
    'version': '1.0.1',
    'category': 'Point Of Sale',
    'author': 'TrendAV',
    'maintainer': 'TrendAV',
    'website': 'http://www.trendav.com',
    'sequence': 21,
    'summary': 'Touchscreen Interface for Shops',
    'description': """
Quick and Easy sale process from PoS - TrendAV for Mimoki
=========================================================
    """,
    'depends': ['trend_point_of_sale'],
    'data': [
             'views/pos_view.xml',
             'views/pos_static.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'qweb': ['static/src/xml/pos.xml',],
    'auto_install': False,
}
