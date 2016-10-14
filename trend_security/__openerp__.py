# -*- coding: utf-8 -*-
{
    'name': 'Trend Security',
    'summary': 'Security and custom profiles for TrendAv',
    'version': '0.1',
    'category': 'Base',
    'description': """
Trend Security
============================================================================================

Features:
---------
    * New groups for custom user profiles
    * New access rights for custom groups
""",
    'author': 'Onawoo Soluciones C.A. (Alexander Rodriguez adrt271988@gmail.com)',
    'website': '',
	'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
    ],
    'depends': [
        'trend_base','trend_stock_mini','pos_graph_custom'
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
