import logging
from odoo.upgrade import util


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    
    modules_to_uninstall = [
        'mollie_account_sync',
        'jt_website_sale_vatprices',
    ]

    for candidate in modules_to_uninstall:
        _logger.info("About to uninstall module %s", candidate)
        util.uninstall_module(cr,candidate)

    util.remove_view(cr, xml_id='jt_now_custom.product2')
    util.remove_view(cr, xml_id='jt_now_custom.product_quantity')
    util.remove_view(cr, xml_id='jt_now_custom.shop_product_carousel_square')
    

