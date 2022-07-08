odoo.define('jt_now_custom.s_video_plyr_options', function (require) {
    'use strict';

    const weWidgets = require('wysiwyg.widgets');
    const options = require('web_editor.snippets.options');

    options.registry.Plyrdata = options.Class.extend({

        /**
         * @override
         */
        willStart: function () {
            var defs = [this._super.apply(this, arguments)];

            var defaults = {
                src540: 'https://notonlywhite.global.ssl.fastly.net/vid/not_only_white-simple_pleasures_created_for_you%20(540p).mp4',
                src720: 'https://notonlywhite.global.ssl.fastly.net/vid/not_only_white-simple_pleasures_created_for_you%20(720p).mp4',
                src1080: 'https://notonlywhite.global.ssl.fastly.net/vid/not_only_white-simple_pleasures_created_for_you%20(1080p).mp4',
            };

            this.videoData = _.defaults(_.pick(this.$target.data(), _.keys(defaults)), defaults);

            return Promise.all(defs).then(() => this._markSectionElement()).then(() => this._refreshPublicWidgets());
        },

        videoSrc540: function (previewMode, widgetValue, params) {
            this.videoData.src540 = widgetValue;
            return this._markSectionElement();
        },
        videoSrc720: function (previewMode, widgetValue, params) {
            this.videoData.src720 = widgetValue;
            return this._markSectionElement();
        },
      
        videoSrc1080: function (previewMode, widgetValue, params) {
            this.videoData.src1080 = widgetValue;
            return this._markSectionElement();
        },
              
      

        /**
         * @override
         */
        _computeWidgetState: function (methodName, params) {
            switch (methodName) {
                case 'videoSrc540': {
                    return this.videoData.src540;
                }
                case 'videoSrc720': {
                    return this.videoData.src720;
                }
                case 'videoSrc1080': {
                    return this.videoData.src1080;
                }
            }
            return this._super(...arguments);
        },

        _markSectionElement: function () {
            return Promise.resolve().then(() => {
                _.each(this.videoData, (value, key) => {
                    this.$target.attr('data-' + key, value);
                    this.$target.data(key, value);
                });
                this._renderSources();
            });
        },

        _renderSources: function () {
            this._renderSource('540', this.videoData.src540);
            this._renderSource('720', this.videoData.src720);
            this._renderSource('1080', this.videoData.src1080);
        },

        _renderSource: function(resolution, sourceValue) {
            // <source type="video/mp4" src="..." size="540"/>
            var query = "source[size='" + resolution + "']";
            var $sourceElement = this.$target.find(query);
            
            if (sourceValue) {                
                if ($sourceElement.length == 0){
                    var $newSourceElement = $('<source/>',{
                        src: sourceValue,
                        type: 'video/mp4',
                        size: resolution,
                    });
                    var $videoEl = this.$target.find("video");
                    
                    $videoEl.append($newSourceElement);                 
                } else {
                    $sourceElement.attr('src', sourceValue);
                }
            } else {
                $sourceElement.remove();
            }
        },

    });

});    