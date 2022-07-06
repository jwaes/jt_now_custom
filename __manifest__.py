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
    'version': '1.15',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'website_sale_stock',
        'sale_management',
        'crm',
        'project',
        'purchase',
        'sale_purchase',
        'jt_mrp_otf',
        'jt_lead_task',
        ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "report/purchase_quotation_templates.xml",
        "report/purchase_order_templates.xml",
        "report/sale_report_templates.xml",
        "views/crm_lead_views.xml",
        "views/ir_qweb_widget_templates.xml",
        "views/portal_templates.xml",
        "views/res_partner_views.xml",
        "views/stock_picking_views.xml",
        "views/product_view.xml",
        "views/webclient_templates.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
    ],

    'assets': {
        'web._assets_primary_variables': [
            'jt_now_custom/static/src/legacy/scss/primary_variables.scss',
        ],
        'web.assets_qweb': [
            'jt_now_custom/static/src/xml/*.xml',
        ],
    },
}
