# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _
from odoo.tools.misc import format_date, get_lang

from dateutil.relativedelta import relativedelta
from itertools import chain


class ReportRoyalty(models.Model):
    _name = "jt.now.report.royalties"
    _description = "Royalties"
    _inherit = 'account.accounting.report'
    # _order = "partner_name, report_date asc, move_name desc"
    _auto = False

    # filter_date = {'mode': 'single', 'filter': 'today'}
    filter_date = {'mode': 'range', 'filter': 'this_month'}
    filter_unfold_all = True
    filter_partner = True
    order_selected_column = {'default': 0}    


    product_id = fields.Many2one('product.product')
    product_name = fields.Char(string='Product name')
    partner_id = fields.Many2one('res.partner')
    partner_name = fields.Char(group_operator='max')
    move_type = fields.Char()
    move_name = fields.Char(group_operator='max')
    move_ref = fields.Char()

    price_subtotal = fields.Monetary(string='Subtotal')
    price_unit = fields.Float(string='Unit price')
    quantity = fields.Float(string='Quantity')

    line_date = fields.Date(group_operator='max', string='Line Date')

    @api.model
    def _get_sql(self):
        options = self.env.context['report_options']
        query = ("""
            SELECT
                {move_line_fields},
                account_move_line.product_id as product_id,
                product.default_code as product_code,
				product_tmpl.name as product_name,
                account_move_line.price_total as price_subtotal,
                account_move_line.price_unit as price_unit,
                account_move_line.quantity as quantity,
                account_move_line.partner_id as partner_id,
                partner.name AS partner_name,
                account_move_line.date as line_date,
                val.name as royalty_name,

                move.move_type AS move_type,
                move.name AS move_name,
                move.ref AS move_ref
				
            FROM account_move_line
            JOIN account_move move ON account_move_line.move_id = move.id
            LEFT JOIN product_product product ON account_move_line.product_id = product.id
			LEFT JOIN product_template product_tmpl ON product.product_tmpl_id = product_tmpl.id
            LEFT JOIN res_partner partner ON partner.id = account_move_line.partner_id
            LEFT JOIN jt_property_kv kv ON product.id = kv.product_id
            LEFT JOIN jt_property_key key ON kv.key_id = key.id
            LEFT JOIN jt_property_value val ON kv.value_id = val.id
			WHERE move_type = 'in_invoice'
                AND code.code = 'internal.royalty'

            """).format(
            move_line_fields=self._get_move_line_fields('account_move_line'),
            # currency_table=self.env['res.currency']._get_query_currency_table(options),
            # period_table=self._get_query_period_table(options),
        )
        params = {
        #     'account_type': options['filter_account_type'],
        #     'sign': 1 if options['filter_account_type'] == 'receivable' else -1,
        #     'date': options['date']['date_to'],
        #     'lang': self.env.user.lang or get_lang(self.env).code,
        }
        return self.env.cr.mogrify(query, params).decode(self.env.cr.connection.encoding)      


    ####################################################
    # COLUMNS/LINES
    ####################################################
    @api.model
    def _get_column_details(self, options):
        columns = [
            self._header_column(),

            self._field_column('partner_name'),
            self._field_column('move_name'),
            self._field_column('line_date'),            
            self._field_column('product_name'),
            self._field_column('quantity'),
            self._field_column('price_unit'),
            self._field_column('price_subtotal'),

        ]

        return columns           

    def _get_hierarchy_details(self, options):
        return [
            self._hierarchy_level('partner_id', foldable=True, namespan=len(self._get_column_details(options)) - 5),
            self._hierarchy_level('id'),
        ]

    def _format_partner_id_line(self, res, value_dict, options):
        res['name'] = value_dict['partner_name'][:128] if value_dict['partner_name'] else _('Unknown Partner')     

    def _format_id_line(self, res, value_dict, options):
        res['name'] = value_dict['move_name']
        res['title_hover'] = value_dict['move_ref']
        # res['caret_options'] = 'account.payment' if value_dict.get('payment_id') else 'account.move'
        for col in res['columns']:
            if col.get('no_format') == 0:
                col['name'] = ''
        res['columns'][-1]['name'] = ''

    def _format_total_line(self, res, value_dict, options):
        res['name'] = _('Total')
        res['colspan'] = len(self._get_column_details(options)) - 5
        res['columns'] = res['columns'][res['colspan']-1:]        