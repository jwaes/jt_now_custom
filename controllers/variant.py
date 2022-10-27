from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController
from odoo.tools.misc import get_lang

class WebsiteSaleStockPropertiesVariantController(WebsiteSaleVariantController):
    @http.route()
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty, **kw):
        kw['context'] = kw.get('context', {})
        combination = super().get_combination_info_website(product_template_id, product_id, combination, add_qty, **kw)
        
        product = request.env['product.product'].sudo().browse(combination['product_id'])

        lang = get_lang(request.env).code

        stockinfo_view = request.env['ir.ui.view'].with_context(lang=lang)._render_template('jt_now_custom.website_sale_product_stockinfo', values={
            'product_variant': product,
        })

        combination['product_stockinfo'] = stockinfo_view

        return combination