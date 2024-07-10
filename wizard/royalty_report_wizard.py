import logging
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.tools import date_utils
import re


_logger = logging.getLogger(__name__)

class RoyaltyReport(models.TransientModel):
    _name = 'jt.now.wizard.royalty.report'
    _description = "Royalty report"

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


    # generate PDF report
    def action_print_report(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to, 
            'royalty_value_id': self.royalty_value_id.id,
            'commission': self.commission,
            'report_id': self.id,
        }
        return self.env.ref('jt_now_custom.action_now_royalty_report').report_action(self.id, data=data)

    # Generate xlsx report
    def action_generate_xlsx_report(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to, 
            'royalty_value_id': self.royalty_value_id.id, 
        }
        # return self.env.ref('openacademy.action_openacademy_xlsx_report').report_action(self, data=data)
        return None



class RoyaltyReportPDF(models.AbstractModel):
    _name = 'report.jt_now_custom.royalty_report_pdf_template'
    _description = "Royalty report PDF"

    def _get_report_values(self, docids, data=None):
        domain = [
            ('parent_state', '=', 'posted'),
            ('move_id.move_type', '=', 'in_invoice'),
            ('display_type', '=', False)
        ]
        if data.get('date_from'):
            domain.append(('date', '>=', data.get('date_from')))
        if data.get('date_to'):
            domain.append(('date', '<=', data.get('date_to')))
        # if data.get('course_ids'):
        #     domain.append(('id', 'in', data.get('course_ids')))

        royalty_value_id = self.env['jt.property.value'].browse(data.get('royalty_value_id'))
        logger.info('royalty_value_id is ', royalty_value_id)

        # docs = self.env['account.move.line'].search(domain)
        lines = self.env['account.move.line'].search(domain).filtered(lambda line: royalty_value_id in line.product_id.royalty_kv_ids.value_id).sorted(key=lambda k: k.date and k.move_name)
        logger.info('lines ', len(lines))
        total = sum(lines.mapped('price_subtotal'))
        commission = data.get('commission')
        total_commission = total * (commission / 100)


        return {
            'doc_ids': lines.ids,
            'docs': lines,
            'royalty_value_id': royalty_value_id,
            'date_from':  data.get('date_from'),
            'date_to':  data.get('date_to'),
            'commission':  data.get('commission'),
            'total': total,
            'total_commission': total_commission,
            'currency_id': self.env.company.currency_id,
        }

