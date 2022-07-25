from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = "product.product"
    
    product_wdh = fields.Boolean("wdh", default=False)
    product_width = fields.Float("width")
    product_depth = fields.Float("depth")
    product_height = fields.Float("height")
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        domain=lambda self: self._get_dimension_uom_domain(),
        help="UoM for width, depth, height",
        default=lambda self: self.env.ref("uom.product_uom_millimeter"),
    )

    is_stock_product = fields.Boolean(compute='_compute_is_stock_product', string='Is stock product')

    lead_time_in_stock = fields.Char(compute='_compute_lead_time_in_stock', string='Lead time in stock')
    lead_time_out_stock = fields.Char(compute='_compute_lead_time_out_stock', string='lead_time_out_stock')
    
    @api.depends('all_kvs')
    def _compute_lead_time_in_stock(self):
        for product in self:
            for kv in product.all_kvs:
                if kv.code == "internal.ships.instock":
                    product.lead_time_in_stock = kv.text
                    return
            product.lead_time_in_stock = "not set"
    
    @api.depends('all_kvs')
    def _compute_lead_time_out_stock(self):
        for product in self: 
            for kv in product.all_kvs:
                if kv.code == "internal.ships.outofstock":
                    product.lead_time_out_stock = kv.text
                    return
            product.lead_time_out_stock = "not set"                    
    
    @api.depends('all_kvs')
    def _compute_is_stock_product(self):
        for product in self: 
            for kv in product.all_kvs:
                if kv.code == "internal.stock":
                    if kv.value_id.code == "stock":
                        product.is_stock_product = True
                        return
            product.is_stock_product = False

    @api.model
    def _get_dimension_uom_domain(self):
        return [("category_id", "=", self.env.ref("uom.uom_categ_length").id)]    
