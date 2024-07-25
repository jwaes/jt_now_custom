/** @odoo-module **/

import VariantMixin from "@website_sale/js/variant_mixin";
import publicWidget from "@web/legacy/js/public/public_widget";

// VariantMixin._onChangeCombinationStockInfo = function (ev, $parent, combination) {

//     let product_id = 0;
//     // needed for list view of variants
//     if ($parent.find('input.product_id:checked').length) {
//         product_id = $parent.find('input.product_id:checked').val();
//     } else {
//         product_id = $parent.find('.product_id').val();
//     }
//     const isMainProduct = combination.product_id &&
//         ($parent.is('.js_main_product') || $parent.is('.main_product')) &&
//         combination.product_id === parseInt(product_id);

//     if (!this.isWebsite || !isMainProduct) {
//         return;
//     }

//     $('div.product_stockinfo').html(combination.product_stockinfo).show(); 

// };

VariantMixin._onChangeCombinationStockInfoFixRemove = function (ev, $parent, combination) {
    $('.oe_website_sale')
        .find('.availability_message_' + combination.product_template_id)
        .remove();
};

publicWidget.registry.WebsiteSale.include({
    /**
     * Adds the vat to the regular _onChangeCombination method
     * @override
     */
    _onChangeCombination: function () {
        VariantMixin._onChangeCombinationStockInfoFixRemove.apply(this, arguments);
        this._super.apply(this, arguments);
        // VariantMixin._onChangeCombinationStockInfo.apply(this, arguments);
    },
});

export default VariantMixin;