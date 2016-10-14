# -*- coding: utf-8 -*-
{
    'name': 'POS Graph Customize',
    'summary': 'New Point of Sale Graph with new filters',
    'version': '0.1',
    'category': 'Point of sale',
    'description': """
POS Graph Customize
============================================================================================

Features:
---------
    * New report graph for POS orders analysis
    * New filters and grouping for/by brands, month, year, weeks

""",
    'author': 'Onawoo Soluciones C.A. (Alexander Rodriguez adrt271988@gmail.com)',
    'website': '',
	'data': [
        'security/ir.model.access.csv',
        'report/pos_order_report_view.xml',
    ],
    'depends': [
        'trend_point_of_sale',
    ],
    'qweb': [
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
