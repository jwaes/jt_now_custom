from odoo import api, fields, models

class Coupon(models.Model):
    _inherit = "coupon.coupon"

    dealer_id = fields.Many2one('res.partner', "Dealer")
    