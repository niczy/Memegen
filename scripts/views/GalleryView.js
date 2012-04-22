define(function(require, exports) {
	var Backbone = require('../libs/backbone.js');
	var $ = require('../libs/jquery.js');
	var MemeCollection = require('../models/MemeCollection.js');

	var GalleryView = Backbone.View.extend({
		events: {
		},

		columnWidth: 250,

        memeThumViews: [],

        columns: [],

		el: '#gallery',

		initialize: function() {
            this.relayout();
		},

		loadMore: function() {
            var MemeThumView = require('./MemeThumView.js');
			console.log("load more called.");
			var memeCollection = new MemeCollection();
            var that = this;
			memeCollection.fetch({
				"success": function(collection, response) {
					collection.each(function(memeModel) {
                        memeThumView = new MemeThumView({
                                model : memeModel,
                                width : that.columnWidth
                        });
                        memeThumView.render();
                        that.memeThumViews.push(memeThumView);
                        $(that.columns[0]).append(memeThumView.el);
                    });
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
            this.columnCount = Math.floor(this.width / this.columnWidth);
            this.render();
		},

		render: function() {
            var GalleryTemplate = require('../templates/GalleryTemplate.js');
            $(this.el).empty();
            for (var i = 0; i < this.columnCount; i++) {
                $(this.el).append(GalleryTemplate.columnTemplate());
            }
            this.columns = this.$('.column');
		}
	});
	return GalleryView;
});

