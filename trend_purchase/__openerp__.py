# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase Management [TrendAV]',
    'version': '1.0.1',
    'category': 'Purchase Management',
    'author': 'Ing. Rigoberto Martínez',
    'maintainer': 'TrendAV',
    'website': 'http://www.trendav.com',
    'sequence': 60,
    'depends': ['purchase'],
    'demo': [
    ],
    'summary': 'Purchase Orders, Receipts, Vendor Bills',
    'description': """
Manage goods requirement by Purchase Orders easily [TrendAV]
============================================================
    """,
    'data': [
        "views/product_view.xml",
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}

