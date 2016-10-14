# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

# Marca
class product_marca(models.Model):
    _name = "product.marca"
    
    name = fields.Char(string="Nombre", index=True, required=True)


# Product Template 
class product_template(models.Model):
    _inherit = "product.template"

    @api.model
    def _get_seq_prod(self):
        args = [('code', '=', 'product.automatic.sequence')]
        rec_s = self.env['ir.sequence'].search(args, limit=1)
        size = rec_s.padding - len(str(rec_s.number_next_actual))
        return ''.join('0' for x in range(size)) + str(rec_s.number_next_actual)

    marca_id = fields.Many2one("product.marca", string="Marca")
    t_discount = fields.Float(string="Discount", default=0.00)
    reference = fields.Char(string="Referencia automática", default=_get_seq_prod)
    
    @api.model
    def create(self, vals):
        obj_seq = self.env['ir.sequence']
        vals['reference'] = obj_seq.next_by_code('product.automatic.sequence')
        return super(product_template, self).create(vals)

# END