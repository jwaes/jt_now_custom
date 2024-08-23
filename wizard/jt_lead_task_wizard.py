import logging
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class CrmLeadTaskWizard(models.TransientModel):
    _inherit = "jt.lead.task.wizard"


    def add_lead_task(self):
        task = super(CrmLeadTaskWizard, self).add_lead_task()
        if task.project_id.otf_bom_template_id:
            _logger.info("found a otf bom template")
            bom = task.project_id.otf_bom_template_id.create_otf_bom_product()
            product = bom.product_id
            if task.partner_id.parent_id:
                product.partner_id = task.partner_id.parent_id
            else :
                product.partner_id = task.partner_id
            product.product_wdh = True
            task.product_id = product
            product.task_id = task
            
            task_prefix = self.env['ir.config_parameter'].sudo().get_param('jt_lead_task.task_prefix')
            task_name = task_prefix + ' ' + product.code
            task.name = task_name

            # add chatter
            # body = 'Created from opportunity ' + task.lead_id.display_name
            # product.message_post(
            #     body=body,
            #     message_type='notification'
            # )

            note_subtype_id = self.env['ir.model.data']._xmlid_to_res_id(
                'mail.mt_note')

            product.message_post_with_source(
                'mail.message_origin_link',
                render_values={'self': product, 'origin': task.lead_id},
                subtype_id=note_subtype_id,
            )            

        else:
            _logger.info("no otf bom template")

        return task