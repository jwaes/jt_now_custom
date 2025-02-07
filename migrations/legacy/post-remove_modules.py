import logging
from odoo.upgrade import util


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    
    modules_to_uninstall = [
        'jt_sale_order_line_codecolumn',
    ]

    for candidate in modules_to_uninstall:
        _logger.info("About to uninstall module %s", candidate)
        util.uninstall_module(cr,candidate)


    util.remove_theme(cr, 'theme_now')

    util.update_record_from_xml(cr, 'sale.mail_template_sale_confirmation' )