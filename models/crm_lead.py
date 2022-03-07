# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    client_ref = fields.Char("Client reference")
    pafin_ref = fields.Char("Pafin reference")
    