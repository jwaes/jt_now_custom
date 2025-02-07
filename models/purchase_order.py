import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class PurchaseOrde(models.Model):
    _inherit = "purchase.order"

    week_planned = fields.Integer(compute='_compute_week_planned')
    
    @api.depends('date_planned')
    def _compute_week_planned(self):
        for order in self:
            if order.date_planned:
                _logger.info("Purchase order planned: ", order.date_planned)
                order.week_planned = order.date_planned.isocalendar()[1]
                _logger.info("Week planned: ", order.week_planned)
            else:
                _logger.warning("Purchase order line has no date planned")
