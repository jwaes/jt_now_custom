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
            action = self.action_new_quotation()
            for task in self.task_ids:
                _logger.info("task thingy")            
            return action