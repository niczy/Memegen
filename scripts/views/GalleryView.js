define(function(require, exports) {
	var Backbone = require('../libs/backbone.js');
	var $ = require('../libs/jquery.js');
    var _ = require('../libs/underscore.js');
	var MemeCollection = require('../models/MemeCollection.js');

	var GalleryView = Backbone.View.extend({
		events: {
		},

		columnWidth: 250,

        memeThumViews: [],

        columns: [],

        columnsHeight: [],

		el: '#gallery',

		initialize: function() {
            this.relayout();
		},

		loadMore: function() {
			console.log("load more called.");
			var memeCollection = new MemeCollection();
            var that = this;
			memeCollection.fetch({"success":
                    function(collection){ 
                        that.appendMemes(collection);
                    }});
		},

        appendMemes: function(memeCollection) {
                        var MemeThumView = require('./MemeThumView.js');
                        var that = this;
                        memeCollection.each(function(memeModel) {
                            memeThumView = new MemeThumView({
                                    model : memeModel,
                                    width : that.columnWidth
                            });
                            memeThumView.render();
                            that.memeThumViews.push(memeThumView);
                            that.renderSingleThum(memeThumView);
                        });
                     },

        click: function() {
                    console.log("element clicked,");

               },

        count: 0,

        renderSingleThum: function(memeThumView) {
                            var minHeight = Number.MAX_VALUE;
                            var targetColumn;
                            _.each(this.columns, function(column) {
                                console.log($(column).height() + " column height");
                                if ($(column).height() < minHeight) {
                                    minHeight = $(column).height();
                                    targetColumn = column;
                                }
                            });
                            $(targetColumn).append(memeThumView.el);
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
            var view = new Backbone.View();
            $(this.el).empty();
            this.columns.length = 0;
            for (var i = 0; i < this.columnCount; i++) {
                var elColumn = view.make("div", {"class": "column"});
                $(this.el).append(elColumn);
                this.columns.push(elColumn);
            }
            var that = this;
            _.each(this.memeThumViews, function(memeThumView) {
                that.renderSingleThum(memeThumView); 
            });
		}
	});
	return GalleryView;
});

