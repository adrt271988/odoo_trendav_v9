# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

# Inherit - Account payment
class trend_pos_account_payment(models.Model):
    _inherit = "account.payment"
    
    is_advance_payment = fields.Boolean('¿Es un pago anticipado?', default=True)
    
    @api.multi
    def revert_payment(self):
        self.copy({'payment_type': 'outbound'})
        self.state = 'sent'
    
    
    