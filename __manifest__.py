# -*- coding: utf-8 -*-
{
    'name': "jt_now_custom",

    'summary': "NOW backend customizations",

    'description': "",

    'author': "jaco tech",
    'website': "https://jaco.tech",
    "license": "AGPL-3",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '15.0.1.0.12',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','project','purchase','sale_purchase','jt_mrp_otf','jt_lead_task'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "report/purchase_quotation_templates.xml",
        "report/purchase_order_templates.xml",
        "views/crm_lead_views.xml",
        "views/res_partner_views.xml",
        "views/stock_picking_views.xml",
        "views/product_view.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
    ],

    'assets': {
        'web._assets_primary_variables': [
            'jt_now_custom/static/src/legacy/scss/primary_variables.scss',
        ],
    },
}
