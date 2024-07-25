/** @odoo-module **/

import VariantMixin from "@website_sale/js/variant_mixin";
import publicWidget from "@web/legacy/js/public/public_widget";

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

    const $pipo = $('.oe_website_sale')
        .find('.availability_message_' + combination.product_template)
    console.log('pipo')
    console.log($pipo)
    const $pipo2 = $('.oe_website_sale')
        .find('.availability_message_' + combination.product_template_id)   
    console.log('$pipo2')
    console.log($pipo2)     

};

publicWidget.registry.WebsiteSale.include({
    /**
     * Adds the vat to the regular _onChangeCombination method
     * @override
     */
    _onChangeCombination: function () {
        combination = arguments[1]
        console.log('combi')
        console.log(combination)
        $('.oe_website_sale')
        .find('.availability_message_' + combination.product_template_id)
        .remove();
        this._super.apply(this, arguments);
        VariantMixin._onChangeCombinationStockInfo.apply(this, arguments);
    },
});

export default VariantMixin;