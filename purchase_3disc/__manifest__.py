# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase 3Disc',
    'version': '1.2',
    'category': 'Inventory/Purchase_3Disc',
    'sequence': 35,
    'summary': 'Purchase orders, tenders and agreements',
    'description': "",
    'website': 'https://www.odoo.com/page/purchase',
    'depends': ['base','account','purchase'],
    'data': [
        'data/initial_3disc_data.xml',
        'data/sequence.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/3disc_department_views.xml',
        'views/3disc_purchase_views.xml',
        'report/purchase_report_3disc.xml',
        'views/res_config_settings_views.xml',
        'views/sequence_views.xml',
    ],
    'qweb': [
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
