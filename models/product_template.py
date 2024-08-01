import logging
import json
from odoo import api, fields, models
from odoo.tools import float_compare


_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_wdh = fields.Boolean("wdh", default=False)
    product_width = fields.Float("width")
    product_depth = fields.Float("depth")
    product_height = fields.Float("height")
    product_packaging_width = fields.Float("packaging width")
    product_packaging_depth = fields.Float("packaging depth")
    product_packaging_height = fields.Float("packaging height")
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        domain=lambda self: self._get_dimension_uom_domain(),
        help="UoM for width, depth, height",
        default=lambda self: self.env.ref("uom.product_uom_millimeter"),
    )
    product_weight = fields.Float("weight")
    product_packaging_weight = fields.Float("packaging weight")
    weight_uom_id = fields.Many2one(
        "uom.uom",
        "Weight dimensional UoM",
        domain=lambda self: self._get_dimension_uom_domain(),
        help="UoM for weight",
        default=lambda self: self.env.ref("uom.product_uom_kgm"),
    )   

    is_dealer_product = fields.Boolean(
        compute='_compute_is_dealer_product', string='is_dealer_product')

    is_custom_made_product = fields.Char(compute='_compute_is_custom_made_product', string='is_custom_made_product')
    
    allow_discount = fields.Boolean('Allow Discount', default=True)

    @api.depends('tmpl_all_kvs')
    def _compute_is_custom_made_product(self):
        for tmpl in self:
            tmpl.is_custom_made_product = False
            for kv in tmpl.tmpl_all_kvs:
                if kv.code == "internal.stock":
                    if kv.value_id.code == "custom-made":
                        tmpl.is_custom_made_product = True
            

    @api.model
    def _get_dimension_uom_domain(self):
        return [("category_id", "=", self.env.ref("uom.uom_categ_length").id)]  

    @api.depends('tmpl_all_kvs')
    def _compute_is_dealer_product(self):
        for tmpl in self:
            tmpl.is_dealer_product = False
            for kv in tmpl.tmpl_all_kvs:
                if kv.code == "internal.stock":
                    if kv.value_id.code == "dealer":
                        tmpl.is_dealer_product = True
            

    # def _get_combination_info(self, combination=False, product_id=False, add_qty=1, parent_combination=False, only_template=False):
    #     combination_info = super(ProductTemplate, self)._get_combination_info(
    #         combination=combination,
    #         product_id=product_id,
    #         add_qty=add_qty,
    #         parent_combination=parent_combination,
    #         only_template=only_template,
    #     )
    #     self.ensure_one()

    #     website = self.env['website'].get_current_website().with_context(self.env.context)

    #     if website:
    #         context = dict(self.env.context, ** {
    #             'quantity': self.env.context.get('quantity', add_qty),
    #             'pricelist': website.pricelist_id.id
    #         })

    #         product = (self.env['product.product'].browse(combination_info['product_id']) or self)   

    #         combination_info.update({
    #             'is_dealer_product': product.is_dealer_product,
    #         })

    #     return combination_info

    def _get_additionnal_combination_info(self, product_or_template, quantity, date, website):
        res = super()._get_additionnal_combination_info(product_or_template, quantity, date, website)

        if not self.env.context.get('website_sale_stock_now'):
            return res

        if product_or_template.is_product_variant:
            product_sudo = product_or_template.sudo()
            res['is_dealer_product'] = product_sudo.is_dealer_product
            res['is_stock_product'] = product_sudo.is_stock_product
            res['lead_time_in_stock'] = product_sudo.lead_time_in_stock
            res['lead_time_out_stock'] = product_sudo.lead_time_out_stock

        return res


    def _is_add_to_cart_possible(self, parent_combination=None):
        self.ensure_one()        
        if self.is_custom_made_product:
            return False
        else:
            return super()._get_possible_combinations(parent_combination)



    def _get_sales_prices(self, pricelist, fiscal_position):
        res = super()._get_sales_prices(pricelist, fiscal_position)
        _logger.info("_get_sales_prices")
        _logger.info(json.dumps(res, sort_keys=True, default=str))
        # for record in self:
        #     _logger.info('_get_sales_prices %s (%s) (%s)', record.name, pricelist.name, fiscal_position.name)   
        #     r = res[record.id]
        #     _logger.info('record name: %s', record.name)
        #     _logger.info(json.dumps(r))
        #     if(record._name == 'product.template' and float_compare(r['price_reduce'], 0.0) == 0):
        #         _logger.info('is template')
        #         r = res[record.product_variant_id.id]
        #         _logger.info(json.dumps(r))

        for template in self:
            if template.product_variant_id:
                _logger.info("template.product_variant_id %s", str(template.product_variant_id.id))
                combination_info = template._get_combination_info(product_id=template.product_variant_id.id)
                _logger.info(json.dumps(combination_info, sort_keys=True, default=str))
                template_price_vals = {
                    'price_reduce': combination_info['price'],
                }
                if combination_info['compare_list_price']:
                    template_price_vals['base_price'] = combination_info['compare_list_price']

                res[template.id] = template_price_vals       


        return res