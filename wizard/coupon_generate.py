from odoo import api, fields, models
import ast

class CouponGenerate(models.TransientModel):
    _inherit = "coupon.generate.wizard"

    dealer_id = fields.Many2one('res.partner', "Dealer")

    def generate_coupon(self):
        """Generates the number of coupons entered in wizard field nbr_coupons
        """
        program = self.env['coupon.program'].browse(self.env.context.get('active_id'))

        vals = {'program_id': program.id}
        if self.dealer_id: 
            vals['dealer_id'] = self.dealer_id.id

        if self.generation_type == 'nbr_coupon' and self.nbr_coupons > 0:
            for count in range(0, self.nbr_coupons):
                self.env['coupon.coupon'].create(vals)

        if self.generation_type == 'nbr_customer' and self.partners_domain:
            for partner in self.env['res.partner'].search(ast.literal_eval(self.partners_domain)):
                vals.update({'partner_id': partner.id, 'state': 'sent' if partner.email else 'new'})
                coupon = self.env['coupon.coupon'].create(vals)
                context = dict(lang=partner.lang)
                subject = _('%s, a coupon has been generated for you') % (partner.name)
                del context
                if self.template_id:
                    email_values = {'email_from': self.env.user.email or '', 'subject': subject}
                    self.template_id.send_mail(coupon.id, email_values=email_values, notif_layout='mail.mail_notification_light')    