define(function(require, exports) {
	var Backbone = require('../libs/backbone.js');
	var $ = require('../libs/jquery.js');
	var MemeThumView = Backbone.View.extend({

		render: function() {
            var view = new Backbone.View();
            this.el = view.make('div');
            $(this.el).css('width', this.options.width);
            var GalleryTemplate = require('../templates/GalleryTemplate');
            var thumData = this.model.toJSON();
            thumData.width = this.options.width;
            $(this.el).html(GalleryTemplate.thumTemplate(thumData));

            console.log(this.model.get('blob_key'));
			console.log(this.el);
		}

	});
	return MemeThumView;
});

