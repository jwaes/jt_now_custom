from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_dealer_product = fields.Boolean(
        compute='_compute_is_dealer_product', string='is_dealer_product')

    @api.depends('tmpl_all_kvs')
    def _compute_is_dealer_product(self):
        for tmpl in self:
            for kv in tmpl.tmpl_all_kvs:
                if kv.code == "internal.stock":
                    if kv.value_id.code == "dealer":
                        tmpl.is_dealer_product = True
                        return
            tmpl.is_dealer_product = False

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            pricelist=pricelist,
            parent_combination=parent_combination,
            only_template=only_template,
        )
        self.ensure_one()

        current_website = False

        if self.env.context.get('website_id'):
            context = dict(self.env.context, ** {
                'quantity': self.env.context.get('quantity', add_qty),
                'pricelist': pricelist and pricelist.id
            })

            product = (self.env['product.product'].browse(combination_info['product_id']) or self)   

            combination_info.update({
                'is_dealer_product': product.is_dealer_product,
            })

        return combination_info            

    # Define all the related fields in product.template with 'readonly=False'
    # to be able to modify the values from product.template.
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        related="product_variant_ids.dimensional_uom_id",
        help="UoM for width, depth, height",
        readonly=False,
    )
    product_width = fields.Float(
        related="product_variant_ids.product_width", readonly=False
    )   
    product_depth = fields.Float(
        related="product_variant_ids.product_depth", readonly=False
    )
    product_height = fields.Float(
        related="product_variant_ids.product_height", readonly=False
    )
    product_wdh = fields.Boolean(
        related="product_variant_ids.product_wdh", readonly=False
    )