define(function(require, exports) {
	var Backbone = require('../libs/backbone.js');
	var $ = require('../libs/jquery.js');
	var MemeCollection = require('../models/MemeCollection.js');

	var GalleryView = Backbone.View.extend({
		events: {
		},
		colomnWidth: 250,
		el: '#gallery',
		initialize: function() {
            this.relayout();
		},

		loadMore: function() {
			console.log("load more called.");
			var memeCollection = new MemeCollection();
			memeCollection.fetch({
				"success": function(collection, response) {
					collection.each(function(memeModel) {});
				}
			});

		},

        click: function() {
                    console.log("element clicked,");

               },

		relayout: function() {
            var position = $(this.el).offset();
			this.width = $(this.el).width();
			this.left = position.left;
			this.right = position.right;
			console.log("we have " + Math.floor(this.width / this.colomnWidth) + " columns");

		},

		render: function() {
			$(this.el).append("Hello world");
		}
	});
	return GalleryView;
});

