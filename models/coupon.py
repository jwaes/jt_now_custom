from odoo import api, fields, models

class Coupon(models.Model):
    _inherit = "coupon.coupon"

    def _get_default_website_id(self):
        # program_website_id = self.program_website_id
        program_website_id = self.env['coupon.program'].browse(self.env.context.get('default_program_id')).website_id
        if program_website_id:
            return program_website_id
        else:
            # Website = self.env['website']
            # websites = Website.search([])
            # return len(websites) == 1 and websites or Website
            return self.env.ref('website.default_website')

    dealer_id = fields.Many2one('res.partner', "Dealer")

    share_link = fields.Char(compute='_compute_share_link', string='share_link')
    
    @api.depends('code')
    def _compute_share_link(self):
        for coupon in self: 
            vals = {
                'coupon_id': coupon.id,
                'program_id': coupon.program_id.id,
                'website_id' : coupon._get_default_website_id().id,
            }
            link = self.env['coupon.share'].create(vals)
            coupon.share_link = link.share_link
    