odoo.define('trend_point_of_sale.point_of_sale', function (require) {
"use strict";
    var Model = require('web.DataModel');
    var ActionManager1 = require('web.ActionManager');
    var core = require('web.core');
    var models = require('point_of_sale.models');
    var _t = core._t;
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    models.load_fields('product.product','marca');
    models.load_fields('res.company','street');
    models.load_fields('res.company','city');
    models.load_fields('res.company','zip');
});
