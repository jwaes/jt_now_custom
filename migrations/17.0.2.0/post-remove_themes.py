import logging
from odoo.upgrade import util


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    
    themes_to_uninstall = [
        # 'theme_now',
    ]

    for candidate in themes_to_uninstall:
        _logger.info("About to uninstall theme %s", candidate)
        util.uninstall_theme(cr, candidate)        

    

