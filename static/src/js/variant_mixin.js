/** @odoo-module **/
import VariantMixin from "@website_sale/js/variant_mixin";
import publicWidget from "@web/legacy/js/public/public_widget";

VariantMixin._onChangeCombinationStockInfoFixRemove = function (ev, $parent, combination) {
    $('.oe_website_sale')
        .find('.availability_message_' + combination.product_template_id)
        .remove();
};

publicWidget.registry.WebsiteSale.include({

    _onChangeCombination: function () {
        VariantMixin._onChangeCombinationStockInfoFixRemove.apply(this, arguments);
        this._super.apply(this, arguments);
    },

});

export default VariantMixin;