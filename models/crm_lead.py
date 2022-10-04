# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    client_ref = fields.Char("Client reference")
    pafin_ref = fields.Char("Pafin reference")

    def action_sale_quotations_newer(self):
        if not self.partner_id:
            return self.env["ir.actions.actions"]._for_xml_id("sale_crm.crm_quotation_partner_action")
        else:
            sale_order_vals = {
                'name': self.env['ir.sequence'].next_by_code('sale.order'),
                'partner_id': self.partner_id.id,
                'source_id': self.source_id.id,
                'opportunity_id': self.id,
                'tag_ids': [(6, 0, self.tag_ids.ids)],
                'company_id': self.company_id.id or self.env.company.id,
                'campaign_id': self.campaign_id.id,
                'origin': self.name,
                'client_order_ref': self.client_ref,
            }
            sale_order = self.env["sale.order"].create(sale_order_vals)

            dropship_route = self.env['stock.location.route'].search([('name', '=', 'Dropship')])

            for task in self.task_ids:
                product = task.product_id
                if product is not None:
                    order_line_vals = {
                        'name': product.display_name,
                        'order_id': sale_order.id,
                        'product_id': product.id,
                        'product_uom_qty': 1.0,
                    }

                    otf_bom_template = product.otf_bom_template
                    if otf_bom_template is not None and dropship_route is not None:
                        if otf_bom_template.dropship:
                            order_line_vals['route_id'] = dropship_route.id

                    order_line = self.env["sale.order.line"].create(order_line_vals)

            view = self.env.ref("sale.view_order_form")

            return {
                "name": "New Quotation",
                "view_mode": "form",
                "view_id": view.id,
                "res_model": "sale.order",
                "type": "ir.actions.act_window",
                "res_id": sale_order.id,
                "context": self.env.context,
            }        

    def action_new_quotation(self):
        action = super(CrmLead, self).action_new_quotation()
        action['context'].update({
            'default_client_order_ref': self.client_ref,
        })
        return action