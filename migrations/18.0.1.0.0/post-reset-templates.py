import logging
from odoo.upgrade import util


_logger = logging.getLogger(__name__)


def migrate(cr, version):


    util.records.update_record_from_xml(cr, 'sale.mail_template_sale_confirmation')
    util.records.update_record_from_xml(cr, 'website_sale.mail_template_sale_cart_recovery')
    util.records.update_record_from_xml(cr, 'sale.mail_template_sale_payment_executed')
    util.records.update_record_from_xml(cr, 'account_followup.email_template_followup_1')
    util.records.update_record_from_xml(cr, 'account.email_template_edi_credit_note')
    util.records.update_record_from_xml(cr, 'account.email_template_edi_invoice')
    util.records.update_record_from_xml(cr, 'account.mail_template_data_payment_receipt')
    util.records.update_record_from_xml(cr, 'purchase.email_template_edi_purchase_done')
    util.records.update_record_from_xml(cr, 'purchase.email_template_edi_purchase')
    util.records.update_record_from_xml(cr, 'purchase.email_template_edi_purchase_reminder')
    util.records.update_record_from_xml(cr, 'stock.mail_template_data_delivery_confirmation')
    util.records.update_record_from_xml(cr, 'portal.mail_template_data_portal_welcome')
    util.records.update_record_from_xml(cr, 'auth_signup.mail_template_user_signup_account_created')
    util.records.update_record_from_xml(cr, 'auth_signup.set_password_email')
    util.records.update_record_from_xml(cr, 'auth_signup.mail_template_data_unregistered_users')
    util.records.update_record_from_xml(cr, 'auth_totp_mail.mail_template_totp_invite')
