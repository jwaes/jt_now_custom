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

    @api.model
    def _get_dimension_uom_domain(self):
        return [("category_id", "=", self.env.ref("uom.uom_categ_length").id)]    
