from odoo import api, fields, models

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    week_planned = fields.Integer(compute='_compute_week_planned', tracking=True)
    
    @api.depends('date_planned')
    def _compute_week_planned(self):
        for rec in self:
            rec.week_planned = rec.date_planned.isocalendar()[1]