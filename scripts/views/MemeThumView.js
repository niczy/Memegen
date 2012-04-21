define(function(require, exports) {
	var Backbone = require('../libs/backbone.js');
	var $ = require('../libs/jquery.js');
	var MemeThumView = Backbone.View.extend({

		render: function() {
			console.log("meme thum view called.");
		}

	});
	return MemeThumView;
});

