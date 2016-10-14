# -*- coding: utf-8 -*-

from openerp import api, fields, models, _, tools, SUPERUSER_ID
import openerp.addons.decimal_precision as dp

# Marca
class product_marca(models.Model):
    _name = "product.marca"
    
    name = fields.Char(string="Nombre", index=True, required=True)

#Product Variants
class trend_product_product(models.Model):
    _inherit = "product.product"

    def name_get(self, cr, user, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        if not len(ids):
            return []

        def _name_get(d):
            name = d.get('name','')
            code = context.get('display_default_code', True) and d.get('default_code',False) or False
            if code:
                name = '[%s] %s' % (code,name)
            return (d['id'], name)

        partner_id = context.get('partner_id', False)
        if partner_id:
            partner_ids = [partner_id, self.pool['res.partner'].browse(cr, user, partner_id, context=context).commercial_partner_id.id]
        else:
            partner_ids = []

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access_rights(cr, user, "read")
        self.check_access_rule(cr, user, ids, "read", context=context)

        result = []
        for product in self.browse(cr, SUPERUSER_ID, ids, context=context):
            variant = ", ".join([v.name for v in product.attribute_value_ids])
            name = variant and "%s (%s)" % (product.name, variant) or product.name
            sellers = []
            if partner_ids:
                if variant:
                    sellers = [x for x in product.seller_ids if (x.name.id in partner_ids) and (x.product_id == product)]
                if not sellers:
                    sellers = [x for x in product.seller_ids if (x.name.id in partner_ids) and not x.product_id]
            if sellers:
                for s in sellers:
                    seller_variant = s.product_name and (
                        variant and "%s (%s)" % (s.product_name, variant) or s.product_name
                        ) or False
                    mydict = {
                              'id': product.id,
                              'name': seller_variant or name,
                              'default_code': s.product_code or product.default_code
                              }
                    temp = _name_get(mydict)
                    if temp not in result:
                        result.append(temp)
            else:
                mydict = {
                          'id': product.id,
                          'name': name,
                          'default_code': product.barcode and product.barcode or product.default_code,
                          }
                result.append(_name_get(mydict))
        return result

    @api.multi
    @api.depends('product_tmpl_id.reference','default_code')
    def get_barcode(self):
        for product in self:
            config = self.env['product.barcode.config'].browse(1)
            if config.on_default_code:
                product.barcode = '%s%s'%(product.default_code,str(product.product_variant_count).zfill(3))
            elif config.on_reference:
                barcode = '%s%s'%(product.product_tmpl_id.reference,str(product.product_variant_count).zfill(3))
                if not product.search_read([('barcode','=',barcode)],['barcode']):
                    product.barcode = barcode

    @api.multi
    @api.depends('lst_price','standard_price')
    def get_markup(self):
        for product in self:
            if product.standard_price != 0.00:
                product.markup = product.lst_price / product.standard_price

    barcode = fields.Char(string='Barcode', help="International Article Number used for product identification.", 
                                compute="get_barcode",oldname='ean13', copy=False,store=True)
    markup = fields.Float('Markup', help="Markup",compute="get_markup")

    def create(self, cr, uid, values, context=None):
        if 'product_tmpl_id' in values:
            template = self.pool.get('product.template').browse(cr, uid, values['product_tmpl_id'], context = context)
            values['default_code'] = template.default_code
        return super(trend_product_product, self).create(cr, uid, values, context=context)



# Product Template 
class trend_product_template(models.Model):
    _inherit = "product.template"

    @api.multi
    @api.depends('list_price','standard_price')
    def get_markup(self):
        for product in self:
            if product.standard_price != 0.00:
                product.markup = product.list_price / product.standard_price

    def default_get(self, cr, uid, fields, context):
        res = super(trend_product_template, self).default_get(cr, uid, fields, context=context)
        if 'taxes_id' in res:
            res['taxes_id'] = []
        return res

    marca_id = fields.Many2one("product.marca", string="Marca")
    t_discount = fields.Float(string="Discount", default=0.00)
    reference = fields.Char(string="Referencia automática", default='/')
    type = fields.Selection([
            ('consu', _('Consumable')), 
            ('service', _('Service')),
            ('product', 'Almacenable'),
        ], index=True, change_default=True,
        default='product',
        track_visibility='always',
        help="A consumable is a product for which you don't manage stock, a service is a non-material product provided by a company or an individual.")
    markup = fields.Float('Markup', help="Markup",compute="get_markup")
    
    @api.model
    def create(self, vals):
        if vals.get('reference', '/') == '/':
            vals['reference'] = self.env['ir.sequence'].next_by_code('product.automatic.sequence') or '/'
        result = super(trend_product_template, self).create(vals)
        return result

class product_barcode_config(models.Model):
    _name="product.barcode.config"

    @api.onchange('on_reference','on_default_code')
    def onchange_check(self):
        if self.on_reference:
            self.on_default_code = False
        if self.on_default_code:
            self.on_reference = False

    name= fields.Char(string="Configuración Código de Barras")
    on_reference = fields.Boolean('Con Referencia Automática', default=False, help="El código de barras se llenará con la referencia automática de las variantes")
    on_default_code = fields.Boolean('Con Referencia Interna', default=False, help="El código de barras se llenará con la referencia interna de las variantes")
