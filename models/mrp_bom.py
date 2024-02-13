import logging
from odoo import api, fields, models, tools

_logger = logging.getLogger(__name__)


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    def update_prices(self):
        super().update_prices()
        self.update_royalty_properties()


    def update_royalty_properties(self):
        for record in self:
            product = record.product_id
            if product:
                for bom_line in record.bom_line_ids:
                    line_product = bom_line.product_id
                    
                    for kv in line_product.all_kvs:
                        # _logger.info("├─ %s : %s ", kv.code, kv.text)
                        if kv.code == ProductProduct.ROYALTY_CODE:

                            if kv.value_id not in product.property_kv_ids.filtered(lambda kv: kv.code == ProductProduct.ROYALTY_CODE).value_id:
                                _logger.info("No royalty property line yet in [%s] %s", line_product.default_code, line_product.name)                                
                                # royalty_code = kv.value_id.code
                                # product.lead_time_out_stock = kv.text
                                # # _logger.info("└─ set %s : %s", product.name, kv.text)
                                # break
                                # new_kv = self.env['jt.property.kv'].create({    
                                #     'key_id': kv.key_id.id,
                                #     'value_id': kv.value_id.id,
                                #     'product_id': product.id
                                # })
                                # product.prproperty_kv_ids.append
                                # self.env['product.product'].write({
                                #     'property_kv_ids': [(4, new_kv.id)]
                                # })
                                product.property_kv_ids = [(0,0,{
                                    'key_id': kv.key_id.id,
                                    'value_id': kv.value_id.id,                                   
                                })]
