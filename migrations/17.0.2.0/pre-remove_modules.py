import logging
from odoo.upgrade import util


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    
    modules_to_uninstall = [
        'mollie_account_sync', 
        'payment_mollie_official', 
        'product_harmonized_system', 
        'product_harmonized_system_delivery', 
        'product_harmonized_system_stock'
    ]

    for candidate in modules_to_uninstall:
        _logger.info("About to uninstall module %s", candidate)
        util.remove_module(cr,candidate)

    

