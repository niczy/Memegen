define(function(require, exports) {
	var Backbone = require('../libs/backbone.js');
	var $ = require('../libs/jquery.js');
	var MemeModel = require('./MemeModel.js');

	var MemeCollection = Backbone.Collection.extend({
		url: '/api/templatelist/popular',
		model: MemeModel,
        parse: function(response) {
            return response;
        }
	});
	return MemeCollection;
});

