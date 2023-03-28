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
    'version': '1.87',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'coupon',
        'documents',
        'sale_coupon',
        'web_editor',
        'website_sale',
        'website_sale_stock',
        'sale_management',
        'crm',
        'project',
        'purchase',
        'sale_purchase',
        'jt_mrp_otf',
        'jt_lead_task',
        'jt_product_properties',
        'jt_product_properties_website',
        'jt_image_tools',
        'jt_sale_order_line_codecolumn',
        'jt_website_sale_vatprices',
        ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "report/coupon_report_templates.xml",
        "report/coupon_report.xml",
        "report/purchase_quotation_templates.xml",
        "report/purchase_order_templates.xml",
        "report/sale_report_templates.xml",
        'wizard/coupon_generate_views.xml',
        'views/coupon_views.xml',
        'views/snippets/s_video_plyr.xml',
        'views/snippets/snippets.xml',
        "views/crm_lead_views.xml",
        "views/documents_templates.xml",
        "views/ir_qweb_widget_templates.xml",
        "views/portal_templates.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
        "views/product_view.xml",
        "views/webclient_templates.xml",
        "views/website_sale.xml",
        "views/website_sale_templates.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
    ],

    'assets': {
        'web._assets_primary_variables': [
            'jt_now_custom/static/src/legacy/scss/primary_variables.scss',
        ],
        'web.assets_backend': [
            'jt_now_custom/static/src/css/documents.css',
        ],
        'web.assets_frontend': [
            'jt_now_custom/static/src/js/**/*',
            'jt_now_custom/static/src/css/**/*',
        ],        
        'web.assets_qweb': [
            'jt_now_custom/static/src/xml/*.xml',
        ],
        'website.assets_wysiwyg': [
            'jt_now_custom/static/src/snippets/s_video_plyr/options.js',
        ],           
    },
}
