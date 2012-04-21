define(function(require, exports) {
	var Backbone = require('../libs/backbone.js');
	var $ = require('../libs/jquery.js');

	var MemeModel = Backbone.Model.extend({
		parse: function(response) {
            return response;
		}
	});
	return MemeModel;
});

