import logging
from odoo.upgrade import util


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    
    modules_to_uninstall = [
        'theme_now',
        'mollie_account_sync', 
        'payment_mollie_official', 

    ]

    modules_to_remove = [
        'product_harmonized_system_delivery', 
        'product_harmonized_system_stock',
        'product_harmonized_system', 
    ]

    for candidate in modules_to_uninstall:
        _logger.info("About to uninstall module %s", candidate)
        util.uninstall_module(cr,candidate)

    for candidate in modules_to_remove:
        _logger.info("About to remove module %s", candidate)
        util.remove_module(cr,candidate)        

    

