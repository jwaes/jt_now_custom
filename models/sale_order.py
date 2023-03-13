import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    applied_coupon_count = fields.Integer(compute='_compute_applied_coupon_count', string='Coupon count')
    
    @api.depends('applied_coupon_ids')
    def _compute_applied_coupon_count(self):
        for sale in self:
            sale.applied_coupon_count = len(sale.applied_coupon_ids)


    def action_view_coupons(self):
        self.ensure_one()
        result = self.env["ir.actions.actions"]._for_xml_id('coupon.coupon_action')
        result['domain'] = [('id', 'in', self.applied_coupon_ids.ids)]
        return result