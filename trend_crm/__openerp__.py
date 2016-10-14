# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'CRM',
    'version': '1.0.1',
    'category': 'Customer Relationship Management',
    'author': 'Ing. Rigoberto Martínez',
    'maintainer': 'TrendAV',
    'depends': ['crm'],
    'sequence': 5,
    'summary': 'Leads, Opportunities, Activities',
    'description': """
This is the base module for managing Leads, Opportunities and Activities in Odoo - TrendAV.
===========================================================================================  """,
    'website': 'http://www.trendav.com',
    'demo': [
    ],
    'data': [
             'views/crm_lead_view.xml'
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
