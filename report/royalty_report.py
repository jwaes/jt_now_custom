import logging
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.tools import date_utils
import re


_logger = logging.getLogger(__name__)


class RoyaltyReportPDF(models.AbstractModel):
    _name = 'report.jt_now_custom.royalty_report_view'
    _description = "Royalty report PDF abs"

    @api.model
    def _get_report_values(self, docids, data=None):
        _logger.info('_get_report_values ...')
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
        _logger.info('royalty_value_id is ', royalty_value_id)

        # docs = self.env['account.move.line'].search(domain)
        lines = self.env['account.move.line'].search(domain).filtered(lambda line: royalty_value_id in line.product_id.royalty_kv_ids.value_id).sorted(key=lambda k: k.date and k.move_name)
        _logger.info('lines ', len(lines))
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

