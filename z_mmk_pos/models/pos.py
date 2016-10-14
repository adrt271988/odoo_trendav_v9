# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

# Partner
class res_partner(models.Model):
    _inherit = "res.partner"
    
    boda = fields.Many2one('res.partner.boda', string="Boda")
    date_boda = fields.Date(string="Fecha boda")

# Boda
class res_partner_boda(models.Model):
    _name = "res.partner.boda"
    
    name = fields.Char(string="Descripción")

# END