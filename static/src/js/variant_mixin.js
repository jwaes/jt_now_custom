/** @odoo-module **/

import VariantMixin from "@website_sale/js/variant_mixin";

const originalOnChangeCombination = VariantMixin._onChangeCombination;
VariantMixin._onChangeCombinationStockInfo = function (ev, $parent, combination) {

    let product_id = 0;
    // needed for list view of variants
    if ($parent.find('input.product_id:checked').length) {
        product_id = $parent.find('input.product_id:checked').val();
    } else {
        product_id = $parent.find('.product_id').val();
    }
    const isMainProduct = combination.product_id &&
        ($parent.is('.js_main_product') || $parent.is('.main_product')) &&
        combination.product_id === parseInt(product_id);

    if (!this.isWebsite || !isMainProduct) {
        return;
    }

    $('div.product_stockinfo').html(combination.product_stockinfo).show();
    originalOnChangeCombination.apply(this, [ev, $parent, combination]);    
};

export default VariantMixin;