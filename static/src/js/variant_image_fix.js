odoo.define('jt_now_custom.variant_image_fix', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');
    
    publicWidget.registry.WebsiteSale.include({
        _updateProductImage: function ($productContainer, displayImage, productId, productTemplateId, newCarousel, isCombinationPossible) {
            var $carousel = $productContainer.find('#o-carousel-product');
            var $mainImgs = $productContainer.find('.product_detail_img, .js_variant_img').filter(':not(.d-none)');
            
            if (!$mainImgs.length || !$mainImgs[0]) {
                console.warn('Product image element not found, skipping image update');
                return;
            }
            
            try {
                return this._super.apply(this, arguments);
            } catch (e) {
                console.warn('Failed to update product image:', e);
            }
        },
    });
});