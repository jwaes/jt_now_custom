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


    def _get_products_price(self, products, *args, **kwargs):
        res = super()._get_products_price(products, *args, **kwargs)
        _logger.info("_get_products_price")
        _logger.info(json.dumps(res, sort_keys=True, default=str))
        # variants = products.filtered(lambda r: r._name == 'product.template').product_variant_id
        # if variants:
        #     variant_res = super()._get_products_price(variants, *args, **kwargs)
        #     for record in res:
        #         res[record.id] = variant_res[record.product_variant_id.id]
        # _logger.info("aftger")
        # _logger.info(json.dumps(res, sort_keys=True, default=str))

        return res
