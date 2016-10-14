# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sales Management [TrendAV]',
    'version': '1.0.1',
    'category': 'Sales Management',
    'author': 'Ing. Rigoberto Martínez',
    'maintainer': 'TrendAV',
    'website': 'http://www.trendav.com',
    'sequence': 15,
    'depends': ['sale'],
    'demo': [
    ],
    'summary': 'Quotations, Sales Orders, Invoicing',
    'description': """
Manage sales quotations and orders [TrendAV]
============================================
    """,
    'data': [
        "views/product_view.xml",
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}

