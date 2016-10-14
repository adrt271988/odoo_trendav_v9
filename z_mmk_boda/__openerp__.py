# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bodas [Mimoki]',
    'version': '1.0.1',
    'category': 'Tools',
    'author': 'Ing. Rigoberto Martínez',
    'maintainer': 'TrendAV',
    'website': 'http://www.trendav.com',
    'sequence': 21,
    'summary': 'Bodas',
    'description': """    """,
    'depends': ['event_sale', 'trend_base', 'trend_stock_mini'],
    'data': [
            'data/product_uom_data.xml',
            'views/boda_view.xml',
            'views/registro_boda_view.xml',
            'views/product_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'application': False,
    'qweb': [],
    'auto_install': False,
}
