# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

# Lead
class crm_lead(models.Model):
    _inherit = "crm.lead"
    
    @api.multi
    def action_crm_send(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        t = ir_model_data.get_object_reference('crm', 'email_template_opportunity_mail')
        template_id = t[1]
        compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'crm.lead',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        })
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

# END