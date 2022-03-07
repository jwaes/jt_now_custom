# -*- coding: utf-8 -*-
{
    'name': "jt_now_custom",

    'summary': "NOW backend customizations",

    'description': "",

    'author': "jaco tech",
    'website': "https://jaco.tech",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '15.0.1.0.4',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','project','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "views/crm_lead_views.xml",
        "views/res_partner_views.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
