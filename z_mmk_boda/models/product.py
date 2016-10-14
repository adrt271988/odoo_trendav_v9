# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

# Product template
class product_template(models.Model):
    _inherit = 'product.template'
    
    event_ok = fields.Boolean(default=False)
    
    @api.onchange('categ_id')
    def onchange_parent_id(self):
        if self.categ_id and self.categ_id.is_rental:
            self.uom_id = self.env.ref('z_mmk_boda.product_uom_rental')
            self.uom_po_id = self.env.ref('z_mmk_boda.product_uom_rental')
        else:
            self.uom_id = self.env.ref('product.product_uom_unit')
            self.uom_po_id = self.env.ref('product.product_uom_unit')


# Product category
class product_category(models.Model):
    _inherit = 'product.category'
    
    is_rental = fields.Boolean(string='¿Es una categoría de alquiler?',
                               default=False)
    
    @api.onchange('parent_id')
    def onchange_parent_id(self):
        self.is_rental = self.parent_id and self.parent_id.is_rental or False
            
    