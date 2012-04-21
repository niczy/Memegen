define(function(require, exports) {
	var Backbone = require('../libs/backbone.js');
	var MakeFromTemplateApp = Backbone.Router.extend({
		initialize: function() {
			console.log(Backbone);
            var GalleryView = require('../views/GalleryView.js');
            var galleryView = new GalleryView({el:'#gallery'});
            window.onresize = function() {
                galleryView.relayout();
            };
            galleryView.loadMore();
            galleryView.render();
		}
	});
	var app = new MakeFromTemplateApp();
	return MakeFromTemplateApp;
});

