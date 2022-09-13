from odoo import api, models

class Http(models.AbstractModel):
    _inherit = 'ir.http'


    @api.model
    def get_frontend_session_info(self):
        session_info = super(Http, self).get_frontend_session_info()
        session_info.update({
            'geoip_country_name': request.session.get('geoip', {}).get('country_name'),
        })
        return session_info    