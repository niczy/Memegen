define(function(require, exports){
    var _ = require('../libs/underscore.js');
    exports.columnTemplate = _.template(
        '<div class="column"></div>');
    exports.thumTemplate = _.template(
        '<img src=/i/serve/<%= blob_key %> style="width:<%= width%>px;" />');
});
