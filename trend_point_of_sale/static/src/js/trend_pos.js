odoo.define('trend_point_of_sale.point_of_sale', function (require) {
"use strict";
    var pos_orders = require('point_of_sale.pos_orders');
    var Model = require('web.DataModel');
    var ActionManager1 = require('web.ActionManager');
    var core = require('web.core');
    var models = require('point_of_sale.models');
    var _t = core._t;
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    models.load_fields('product.product','marca');
});