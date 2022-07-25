from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController

class WebsiteSaleStockPropertiesVariantController(WebsiteSaleVariantController):
    @http.route()
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty, **kw):
        kw['context'] = kw.get('context', {})
        combination = super().get_combination_info_website(product_template_id, product_id, combination, add_qty, **kw)
        
        product = request.env['product.product'].browse(combination['product_id'])

        stockinfo_view = request.env['ir.ui.view']._render_template('jt_now_custom.website_sale_product_stockinfo', values={
            'product_variant': product,
        })

        combination['product_stockinfo'] = stockinfo_view

        return combination