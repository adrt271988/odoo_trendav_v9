# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Create Tasks from SO [TrendAV]',
    'version': '1.0.1',
    'category': 'Project Management',
    'author': 'Ing. Rigoberto Martínez',
    'maintainer': 'TrendAV',
    'website': 'http://www.trendav.com',
    'sequence': 15,
    'depends': ['sale_service'],
    'demo': [
    ],
    'description': """
Automatically creates project tasks from procurement lines  [TrendAV]
=====================================================================
    """,
    'data': [
        "views/product_view.xml",
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
