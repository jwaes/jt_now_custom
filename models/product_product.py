import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"
    _order = 'websequence, priority desc, default_code, name, id'
    
    websequence = fields.Integer('Web sequence', default=1, help='Give extra order for website variants')

    is_stock_product = fields.Boolean(compute='_compute_is_stock_product', string='Is stock product')
    is_pickup_product = fields.Boolean(compute='_compute_is_pickup_product', string='Is pickup product')
    
    lead_time_in_stock = fields.Char(compute='_compute_lead_time_in_stock', string='Lead time in stock')
    lead_time_out_stock = fields.Char(compute='_compute_lead_time_out_stock', string='lead_time_out_stock')
    
    @api.depends('all_kvs','all_kvs.text')
    def _compute_lead_time_in_stock(self):
        for product in self:
            # _logger.info("┌── %s ", product.name)
            product.lead_time_in_stock = "not set"
            for kv in product.all_kvs:
                # _logger.info("├─ %s : %s ", kv.code, kv.text)
                if kv.code == "internal.ships.instock":
                    product.lead_time_in_stock = kv.text
                    # _logger.info("└─ set %s : %s", product.name, kv.text)
                    break

    
    @api.depends('all_kvs', 'all_kvs.text')
    def _compute_lead_time_out_stock(self):
        for product in self:
            # _logger.info("┌── %s ", product.name)
            product.lead_time_out_stock = "not set"
            for kv in product.all_kvs:
                # _logger.info("├─ %s : %s ", kv.code, kv.text)
                if kv.code == "internal.ships.outofstock":
                    product.lead_time_out_stock = kv.text
                    # _logger.info("└─ set %s : %s", product.name, kv.text)
                    break
                    
    
    @api.depends('all_kvs')
    def _compute_is_stock_product(self):
        for product in self: 
            for kv in product.all_kvs:
                if kv.code == "internal.stock":
                    if kv.value_id.code == "stock":
                        product.is_stock_product = True
                        return
            product.is_stock_product = False

    @api.depends('all_kvs')
    def _compute_is_pickup_product(self):
        for product in self: 
            for kv in product.all_kvs:
                if kv.code == "internal.delivery.noweu":
                    if kv.value_id.code == "pickup":
                        product.is_pickup_product = True
                        return
            product.is_pickup_product = False            

    @api.model
    def _get_dimension_uom_domain(self):
        return [("category_id", "=", self.env.ref("uom.uom_categ_length").id)]    


    # Define all the related fields in product.template with 'readonly=False'
    # to be able to modify the values from product.template.
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        related="product_tmpl_id.dimensional_uom_id",
        help="UoM for width, depth, height",
        readonly=False,
    )
    product_width = fields.Float(
        related="product_tmpl_id.product_width", readonly=True
    )   
    product_depth = fields.Float(
        related="product_tmpl_id.product_depth", readonly=True
    )
    product_height = fields.Float(
        related="product_tmpl_id.product_height", readonly=True
    )
    product_wdh = fields.Boolean(
        related="product_tmpl_id.product_wdh", readonly=True
    )        

    product_packaging_width = fields.Float(
        related="product_tmpl_id.product_packaging_width", readonly=True
    )   
    product_packaging_depth = fields.Float(
        related="product_tmpl_id.product_packaging_depth", readonly=True
    )
    product_packaging_height = fields.Float(
        related="product_tmpl_id.product_packaging_height", readonly=True
    )
    weight_uom_id = fields.Many2one(
        "uom.uom",
        "Weight dimensional UoM",
        related="product_tmpl_id.weight_uom_id",
        help="UoM for weight",
        readonly=True,
    )    
    product_weight = fields.Float(
        related="product_tmpl_id.product_weight", readonly=True
    )   
    product_packaging_weight = fields.Float(
        related="product_tmpl_id.product_packaging_weight", readonly=True
    )   
