from odoo import api, fields, models

class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    their_ref= fields.Char("Their reference")

    dealer_coupon_ids = fields.One2many('coupon.coupon', 'dealer_id', string="Dealer Coupons", copy=False)

    dealer_coupon_count = fields.Char(compute='_compute_dealer_coupon_count', string='Dealer Coupon Count')
    
    @api.depends('dealer_coupon_ids')
    def _compute_dealer_coupon_count(self):
        for partner in self:
            partner.dealer_coupon_count = len(partner.dealer_coupon_ids)

    def action_view_coupons(self):
        self.ensure_one()
        result = self.env["ir.actions.actions"]._for_xml_id('coupon.coupon_action')
        result['domain'] = [('id', 'in', self.dealer_coupon_ids.ids)]
        return result            