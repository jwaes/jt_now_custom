import logging
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.tools import date_utils
import re


_logger = logging.getLogger(__name__)

class RoyaltyReport(models.TransientModel):
    _name = 'jt.now.wizard.royalty'
    _description = "Royalty wizard"

    period = fields.Selection([
        ('this_month', 'This month'),
        ('last_month', 'Last month'),
        ('custom', 'Custom'),
    ], default='last_month', string='Period')

    date_from = fields.Date('Date from', required=True)
    date_to = fields.Date('Date to', required=True)

    royalty_value_id = fields.Many2one('jt.property.value', string='Royalty value', domain="[('key_id.code', '=', 'internal.royalty')]")

    commission = fields.Float('Commission', default=5.5)

    report_name = fields.Char(compute='_compute_report_name', string='report_name')
    
    @api.depends('date_from', 'date_to', 'royalty_value_id')
    def _compute_report_name(self):
        pattern = r'[^0-9a-zA-Z\s]+'
        roy = re.sub(pattern, "", self.royalty_value_id.name)
        report_name = 'RoyaltyReport_{date_from}_{date_to}_{roy}'.format(date_from=self.date_from, date_to=self.date_to, roy=roy)

    @api.onchange('period')
    def _onchange_period(self):
        today = fields.Date.today()
        last_month = today + relativedelta(months=-1)

        if self.period == 'last_month':
            self.date_from = date_utils.start_of(last_month, 'month')
            self.date_to = date_utils.end_of(last_month, 'month')    
        elif self.period == 'this_month':
            self.date_from = date_utils.start_of(today, 'month')
            self.date_to = today                

    def _prepare_report_data(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to, 
            'royalty_value_id': self.royalty_value_id.id,
            'commission': self.commission,
            'report_id': self.id,
        }
        return data

    # generate PDF report
    def action_print_report(self):
        self.ensure_one()
        _logger.info('action_print_report ...')
        data = self._prepare_report_data()
        return self.env.ref('jt_now_custom.royalty_details_report').report_action([], data=data)

    # # Generate xlsx report
    # def action_generate_xlsx_report(self):
    #     data = {
    #         'date_from': self.date_from,
    #         'date_to': self.date_to, 
    #         'royalty_value_id': self.royalty_value_id.id, 
    #     }
    #     # return self.env.ref('openacademy.action_openacademy_xlsx_report').report_action(self, data=data)
    #     return None

