from odoo import api, fields, models

class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    their_ref= fields.Char("Their reference")
    