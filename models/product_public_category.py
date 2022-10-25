from odoo import api, fields, models

class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    hidden = fields.Boolean('hidden', default=False)