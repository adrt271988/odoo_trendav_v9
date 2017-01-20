# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Base [TrendAV]',
    'version': '1.0.1',
    'category': 'Hidden',
    'author': 'Ing. Rigoberto Martínez',
    'maintainer': 'TrendAV',
    'website': 'http://www.trendav.com',
    'sequence': 1,
    'description': """
Update Odoo - TrendAV, needed for all installation.
===================================================
""",
    'depends': ['base','product','account','board','base_vat'],
    'data': [
             'static/src/xml/base_static.xml',
             'views/base_menu.xml',
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
