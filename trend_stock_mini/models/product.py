# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

# Product template
class product_template(models.Model):
    _inherit = 'product.template'
    
    @api.model
    def default_get(self, fields):
        rec = super(product_template, self).default_get(fields)
        rec['type'] = 'product'
        return rec
    
# Stock picking
class stock_picking(models.Model):
    _inherit = 'stock.picking'
    _order = 'id desc'
    
    pay_term_id = fields.Many2one('account.payment.term', string='Plazo de pago', 
                                  index=True, ondelete='cascade')
    
# Stock move
class stock_move(models.Model):
    _inherit = 'stock.move'
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id: 
            self.product_uom = self.product_id.uom_id.id
            self.name = self.product_id.name
    