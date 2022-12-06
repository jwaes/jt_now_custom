from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    week_planned = fields.Integer(compute='_compute_week_planned')
    
    @api.depends('date_planned')
    def _compute_week_planned(self):
        for rec in self:
            if rec.date_planned:
                _logger.info("Purchase order line date planned: ", rec.date_planned)
                rec.week_planned = rec.date_planned.isocalendar()[1]
                _logger.info("Week planned: ", rec.week_planned)
            else:
                _logger.warning("Purchase order line has no date planned")
