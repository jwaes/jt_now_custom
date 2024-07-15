import logging
import json
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
        _logger.info('docids ', str(docids))
        _logger.info(json.dumps(data))
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
        
        _logger.info('value id ', data.get('royalty_value_id'))
        _logger.info('before')
        royalty_value_id = self.env['jt.property.value'].browse(data.get('royalty_value_id'))
        _logger.info('after')
        _logger.info(str(royalty_value_id.ids))
        # docs = self.env['account.move.line'].search(domain)

        lines = self.env['account.move.line'].search(domain)
        _logger.info('after query')
        _logger.info('lines %s ', len(lines))
        lines = lines.filtered(lambda line: royalty_value_id in line.product_id.royalty_kv_ids.value_id)
        _logger.info('after filtered')
        _logger.info('lines %s ', len(lines))
        lines = lines.sorted(key=lambda k: k.date and k.move_name)
        _logger.info('after sorted')
        _logger.info('lines %s ', len(lines))
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

