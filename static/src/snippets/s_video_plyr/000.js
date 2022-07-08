odoo.define('jt_now_custom.s_video_plyr', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    var utils = require('web.utils');

    const PlyrWidget = publicWidget.Widget.extend({
        selector: '.s_video_plyr',
        disabledInEditableMode: false,

        /**
         * @override
         */
        start: function () {
            var def = this._super.apply(this, arguments);
            
            this.options.wysiwyg && this.options.wysiwyg.odooEditor.observerUnactive();            

            var params = _.pick(this.$el.data(), 'src540', 'src720', 'src1080',);
            if (!params.href) {
                return def;
            }
            
            this.options.wysiwyg && this.options.wysiwyg.odooEditor.observerActive();
            return def;
        },

        /**
         * @override
         */
        destroy: function () {
            this._super.apply(this, arguments);

            // this.options.wysiwyg && this.options.wysiwyg.odooEditor.observerUnactive();

            // this.options.wysiwyg && this.options.wysiwyg.odooEditor.observerActive();            
        },
    });

    publicWidget.registry.Plyrdata = PlyrWidget;

    return PlyrWidget;
});


if (!$('html').attr('data-editable')) {
    const plyrs = Plyr.setup('.js-player');
};
