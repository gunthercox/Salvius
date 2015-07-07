/*!
 * jQuery Network Camera v0.0.1
 * (https://github.com/gunthercox/jquery-network-camera)
 * Copyright 2015 Gunther Cox
 * Licensed under the MIT license
 */

;(function ($, window, document, undefined) {

    var pluginName = 'networkCamera';

    var streaming = true;

    function Plugin (element, options) {
        this.element = element;
        this._name = pluginName;
        this._defaults = $.fn.networkCamera.defaults;

        this.options = $.extend({}, this._defaults, options);

        if (!this.options.url) {
            $.error('The url parameter is required to initialize camera feed.');
        }

        streaming = this.options.stream;

        this.init();
    }

    $.extend(Plugin.prototype, {

        // Initialization logic
        init: function () {
            this.buildCache();
            this.bindEvents();

            var self = this;

            var timer = null;
            var count = 0;
            var image = null;

            var $canvas = $('<canvas/>', {'width': '100%', 'height': '100%'});
            var drawingCanvas = $canvas[0];

            function reload() {
	            image = new Image();
	            image.onload = load;
	            image.src = self.options.url + "?u=" + count;
	            count++;
            }

            function load() {
	            if (drawingCanvas.getContext) {
		            var context = drawingCanvas.getContext("2d");
		            context.drawImage(image,0,0,640,480,0,0,300,150);
	            }

                if (streaming) {
	                setTimeout(reload, timer);
                }
            }

            setTimeout(reload, timer);

            this.$element.html($canvas);

        },

        // Remove plugin instance completely
        destroy: function() {
            this.unbindEvents();
            this.$element.removeData();
        },

        // Cache DOM nodes for performance
        buildCache: function () {
            this.$element = $(this.element);
        },

        // Bind events that trigger methods
        bindEvents: function() {
            var plugin = this;

            // Pause the image stream when clicked
            plugin.$element.on('click'+'.'+plugin._name, function() {
                plugin.toggle.call(plugin);
            });
        },

        // Unbind events that trigger methods
        unbindEvents: function() {
            /*
                Unbind all events in our plugin's namespace that are attached
                to "this.$element".
            */
            this.$element.off('.'+this._name);
        },

        toggle: function() {
            if (streaming) {
                this.pause()
            } else {
                this.stream()
            }
        },

        // Pause the image stream
        pause: function() {
            streaming = false;
            this.$element.trigger('pause');
        },

        // Start streaming the camera images
        stream: function() {
            streaming = true;
            this.init();
            this.$element.trigger('stream');
        }

    });


    /*
        Create a lightweight plugin wrapper around the "Plugin" constructor,
        preventing against multiple instantiations.

        More: http://learn.jquery.com/plugins/basic-plugin-creation/
    */
    $.fn.networkCamera = function (options) {

        this.each(function() {
            if (!$.data(this, "plugin_" + pluginName)) {
                /*
                    Use "$.data" to save each instance of the plugin in case
                    the user wants to modify it. Using "$.data" in this way
                    ensures the data is removed when the DOM element(s) are
                    removed via jQuery methods, as well as when the userleaves
                    the page. It's a good way to prevent memory leaks.

                    More: http://api.jquery.com/jquery.data/
                */
                $.data(this, "plugin_" + pluginName, new Plugin(this, options));
            } else {

                var plugin = $.data(this, "plugin_" + pluginName);

                // Execute methods

                if (options == 'pause') {
                    plugin.pause();
                }

                if (options == 'stream') {
                    plugin.stream();
                }

                if (options == 'toggle') {
                    plugin.toggle();
                }
            }
        });
        /*
            "return this;" returns the original jQuery object. This allows
            additional jQuery methods to be chained.
        */
        return this;
    };

    /*
        Attach the default plugin options directly to the plugin object. This
        allows users to override default plugin options globally, instead of
        passing the same option(s) every time the plugin is initialized.

        More: http://learn.jquery.com/plugins/advanced-plugin-concepts/
    */
    $.fn.networkCamera.defaults = {
        url: null,
        stream: true
    };

})(jQuery, window, document);
