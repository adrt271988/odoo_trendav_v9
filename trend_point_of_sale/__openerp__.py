# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Point of Sale [TrendAV]',
    'version': '1.0.1',
    'category': 'Point Of Sale',
    'author': 'Ing. Rigoberto Martínez',
    'maintainer': 'TrendAV',
    'website': 'http://www.trendav.com',
    'sequence': 20,
    'summary': 'Touchscreen Interface for Shops',
    'description': """
Quick and Easy sale process from PoS - TrendAV
==============================================
    """,
    'depends': ['point_of_sale','trend_product'],
    'data': [
             'views/product_pos_view.xml',
             'views/pos_menu.xml',
             'views/templates.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'application': False,
    'qweb': ['static/src/xml/pos.xml'],
    'auto_install': False,
}
