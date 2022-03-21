from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Define all the related fields in product.template with 'readonly=False'
    # to be able to modify the values from product.template.
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        related="product_variant_ids.dimensional_uom_id",
        help="UoM for width, depth, height",
        readonly=False,
    )
    product_width = fields.Float(
        related="product_variant_ids.product_width", readonly=False
    )   
    product_depth = fields.Float(
        related="product_variant_ids.product_depth", readonly=False
    )
    product_height = fields.Float(
        related="product_variant_ids.product_height", readonly=False
    )
    product_wdh = fields.Boolean(
        related="product_variant_ids.product_wdh", readonly=False
    )
 