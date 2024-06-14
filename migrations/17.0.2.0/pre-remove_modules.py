import logging
from odoo.upgrade import util


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    
    modules_to_uninstall = [
        'mollie_account_sync', 
    ]

    for candidate in modules_to_uninstall:
        _logger.info("About to uninstall module %s", candidate)
        util.modules.uninstall_module(cr,candidate)

    # for candidate in themes_to_uninstall:
    #     _logger.info("About to uninstall theme %s", candidate)
    #     util.uninstall_theme(cr,candidate)

    util.records.remove_view(cr, xml_id='product2')
    util.records.remove_view(cr, xml_id='product_quantity')
    

