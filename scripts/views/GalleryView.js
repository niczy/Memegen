define(function(require, exports) {
	var Backbone = require('../libs/backbone.js');
	var $ = require('../libs/jquery.js');

	var GalleryView = Backbone.View.extend({
		el: '#gallery',
		render: function() {
			$(this.el).append("Hello world");
		}
	});
	return GalleryView;
});

