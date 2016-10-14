odoo.define('z_mmk_pos.models', function (require) {
"use strict";

var pos_db = require('point_of_sale.DB');
var pos_models = require('point_of_sale.models');

var models = pos_models.PosModel.prototype.models;
console.log(models);
for (var i = 0; i < models.length; i++) {
    var model = models[i];
    if (model.model == 'res.partner') {
	//console.log(models[i]);
	models[i].fields.push('boda')
	models[i].fields.push('date_boda');
	//console.log(models[i]);
    }
}


pos_db.include({
    _partner_search_string: function(partner) {
        var str = this._super(partner);
		str = str.replace('\n', '');
        if(partner.boda) { str += '|' + partner.boda; }
        if(partner.date_boda){ str += '|' + partner.date_boda; }
        return str + '\n';
    },
});

});
