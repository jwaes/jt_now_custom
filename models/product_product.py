import logging
import re
from odoo import api, fields, models
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"
    _order = 'websequence, priority desc, default_code, name, id'
    
    websequence = fields.Integer('Web sequence', default=1, help='Give extra order for website variants')

    is_stock_product = fields.Boolean(compute='_compute_is_stock_product', string='Is stock product')
    is_pickup_product = fields.Boolean(compute='_compute_is_pickup_product', string='Is pickup product')
    
    lead_time_in_stock = fields.Char(compute='_compute_lead_time_in_stock', string='Lead time in stock')
    lead_time_out_stock = fields.Char(compute='_compute_lead_time_out_stock', string='Lead time out stock')

    google_shipping_label = fields.Char(compute='_compute_google_shipping_label', string='Google Shipping Label')
    google_return_policy_label = fields.Char(compute='_compute_google_return_policy_label', string='Google Return Policy Label')

    lead_date_out_stock_string = fields.Char(compute='_compute_lead_date_out_stock', string='Lead date out stock iso')
    
    @api.depends('is_stock_product')
    def _compute_google_return_policy_label(self):
        for product in self:
            product.google_return_policy_label = None
            if not product.is_stock_product:
                product.google_return_policy_label = "personalized"

    @api.depends('lead_time_out_stock')
    def _compute_lead_date_out_stock(self):
        digit_pattern = r'\d'
        for product in self:
            match = re.search(digit_pattern, product.lead_time_out_stock)
            weeks = 1
            if match:
                weeks = int(match.group())
                _logger.debug("MATCH : %s", weeks)
            goal = datetime.now() + timedelta(weeks = weeks)
            _logger.debug("GOAL : %s", goal)
            product.lead_date_out_stock_string = goal.isoformat()
            
    
    @api.depends('all_kvs','all_kvs.text')
    def _compute_google_shipping_label(self):
        for product in self:
            product.google_shipping_label = "free"
            for kv in product.all_kvs:
                if kv.code == "internal.delivery.noweu":
                    product.google_shipping_label = kv.value_id.code
                    break
    
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
            product.is_stock_product = False
            _logger.info("┌── %s ", product.name)
            for kv in product.all_kvs:
                # _logger.info("├─ %s : %s ", kv.code, kv.text)
                if kv.code == "internal.stock":
                    _logger.info("└─ %s : %s", product.name, kv.value_id.code)
                    if kv.value_id.code == "stock":
                        product.is_stock_product = True
                        _logger.info("└─ set is_stock_product = True")
                        # return
            

    @api.depends('all_kvs')
    def _compute_is_pickup_product(self):
        for product in self:
            product.is_pickup_product = False
            for kv in product.all_kvs:
                if kv.code == "internal.delivery.noweu":
                    if kv.value_id.code == "pickup":
                        product.is_pickup_product = True
                        

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
