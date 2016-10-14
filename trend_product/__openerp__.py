# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Products & Pricelists [TrendAV]',
    'version': '1.0.1',
    'category': 'Hidden',
    'author': 'Ing. Rigoberto Martínez',
    'maintainer': 'TrendAV',
    'website': 'http://www.trendav.com',
    'sequence': 2,
    'depends': ['trend_base'],
    'demo': [],
    'description': """
This is the base module for managing products in Odoo - TrendAV.
================================================================
    """,
    'data': [
        'security/ir.model.access.csv',
        "data/product_barcode_config.xml",
        "views/product_barcode_config_view.xml",
        "views/product_view.xml",
        "data/sequence_data.xml",
        "report/report_productlabel.xml",
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
