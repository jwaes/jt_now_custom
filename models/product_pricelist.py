import logging
import re
import json
from odoo import api, fields, models
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class Pricelist(models.Model):
    _inherit = "product.pricelist"

    def _get_applicable_rules_domain(self, products, date, **kwargs):
        res = super()._get_applicable_rules_domain(products, date, **kwargs)
        _logger.info("_get_applicable_rules_domain")
        _logger.info(json.dumps(res, sort_keys=True, default=str))
        return res
