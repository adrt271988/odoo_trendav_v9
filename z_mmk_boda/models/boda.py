# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

# Boda
class event_boda(models.Model):
    _inherit = 'event.event'
    
#     invited_ids = fields.Many2many('res.partner', string='Invitados')
#     product_ids = fields.Many2many('product.product', string='Productos',
#                                 domain=[('event_ok', '=', True)], readonly=True)
    place = fields.Char(string='Población')
    registration_ids = fields.One2many('event.registration', 'event_id', 
                                       string='Alquiler a invitados', copy=True)
    
    @api.onchange('registration_ids')
    def onchange_rental_prod_id(self):
        if self.registration_ids:
            preg = [r.rental_prod_id.id for r in self.registration_ids]
            self.product_ids = [(6, False, preg)]

# Registro
class event_registration_boda(models.Model):
    _inherit = 'event.registration'
    
    event_id = fields.Many2one('event.event', string='Event', required=False, 
                               ondelete='cascade')
    rental_prod_id = fields.Many2one('product.product', string='Productos')
    reference_prod = fields.Char(related='rental_prod_id.default_code', 
                                 string='Referencia')
    description_prod = fields.Char(related='rental_prod_id.name', 
                                   string='Descripción')
    qty_availability = fields.Integer(string='Disponibles', readonly=True)
    qty_to_reserve = fields.Integer(string='A reservar', default=1)
        
#     @api.onchange('rental_prod_id')
#     def onchange_rental_prod_id(self): 
#         ini = self.date_open or self.event_id and self.event_id.date_begin
#         fin = self.date_closed or self.event_id and self.event_id.date_end
#         args = ['|', '&', ('date_open', '<=', ini), ('date_closed', '>=', ini),
#                 '&', ('date_open', '<=', fin), ('date_closed', '>=', fin),
#                 ('rental_prod_id', '=', self.rental_prod_id.id)]
#         prod_reserved = sum(r.qty_to_reserve for r in self.search(args))
#         self.qty_availability = self.rental_prod_id.qty_available - prod_reserved
#         self.qty_to_reserve = self.qty_availability > 0 and 1 or 0

    @api.model
    def default_get(self, fields):
        rec = super(event_registration_boda, self).default_get(fields)
        c = self._context or {}
        if 'date_open' in c: rec['date_open'] = c.get('date_open')
        if 'date_closed' in c: rec['date_closed'] = c.get('date_closed')
        return rec
    
# END