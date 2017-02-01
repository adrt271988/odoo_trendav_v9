# -*- coding: utf-8 -*-
import re
from openerp import api, fields, models, _, tools, SUPERUSER_ID
from openerp.osv import expression
import openerp.addons.decimal_precision as dp

# Marca
class product_marca(models.Model):
    _name = "product.marca"
    
    name = fields.Char(string="Nombre", index=True, required=True)

#Product Variants
class trend_product_product(models.Model):
    _inherit = "product.product"

    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        #~ result = super(trend_product_product, self).name_search(cr, user, name=name, args=args, operator=operator, context=context, limit=limit)
        if context is None:
            context = {}
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            ids = []
            if operator in positive_operators:
                ids = self.search(cr, user, [('default_code','=',name)]+ args, limit=limit, context=context)
                if not ids:
                    ids = self.search(cr, user, [('barcode','=',name)]+ args, limit=limit, context=context)
            if not ids and operator not in expression.NEGATIVE_TERM_OPERATORS:
                # Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
                # on a database with thousands of matching products, due to the huge merge+unique needed for the
                # OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
                # Performing a quick memory merge of ids in Python will give much better performance
                ids = self.search(cr, user, args + [('default_code', operator, name)], limit=limit, context=context)
                if not limit or len(ids) < limit:
                    # we may underrun the limit because of dupes in the results, that's fine
                    limit2 = (limit - len(ids)) if limit else False
                    ids += self.search(cr, user, args + [('name', operator, name), ('id', 'not in', ids)], limit=limit2, context=context)
            elif not ids and operator in expression.NEGATIVE_TERM_OPERATORS:
                ids = self.search(cr, user, args + ['&', ('default_code', operator, name), ('name', operator, name)], limit=limit, context=context)
            if not ids and operator in positive_operators:
                ptrn = re.compile('(\[(.*?)\])')
                res = ptrn.search(name)
                if res:
                    ids = self.search(cr, user, [('default_code','=', res.group(2))] + args, limit=limit, context=context)
            # still no results, partner in context: search on supplier info as last hope to find something
            if not ids and context.get('partner_id'):
                supplier_ids = self.pool['product.supplierinfo'].search(
                    cr, user, [
                        ('name', '=', context.get('partner_id')),
                        '|',
                        ('product_code', operator, name),
                        ('product_name', operator, name)
                    ], context=context)
                if supplier_ids:
                    ids = self.search(cr, user, [('product_tmpl_id.seller_ids', 'in', supplier_ids)], limit=limit, context=context)
            if not ids:
                marca_ids = self.pool['product.marca'].search(cr, user, [('name',operator,name)])
                if marca_ids:
                    ids = self.search(cr, user, [('product_tmpl_id.marca_id','in',marca_ids)], context = context)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        result = self.name_get(cr, user, ids, context=context)
        return result

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
            if not product.barcode:
                config = self.env['product.barcode.config'].browse(1)
                for i in range(product.product_variant_count):
                    if config.based_on == "default_code":
                        product.barcode = '%s%s'%(product.default_code,str(i).zfill(3))
                    else:
                        reference = product.product_tmpl_id.reference
                        if reference is False:
                            reference = product.default_code and product.default_code or ''
                        barcode = '%s%s'%(reference,str(i).zfill(3))
                        product.barcode = barcode

    @api.multi
    @api.depends('lst_price','standard_price')
    def get_markup(self):
        for product in self:
            if product.standard_price != 0.00:
                product.markup = product.lst_price / product.standard_price

    @api.multi
    @api.depends('product_tmpl_id.marca_id')
    def get_marca(self):
        for product in self:
            if product.product_tmpl_id and product.product_tmpl_id.marca_id:
                product.marca = product.product_tmpl_id.marca_id.name

    barcode = fields.Char(string='Barcode', help="International Article Number used for product identification.", 
                                compute="get_barcode",oldname='ean13', copy=False,store=True)
    markup = fields.Float('Markup', help="Markup",compute="get_markup")
    marca = fields.Char('Marca', help="Marca",compute="get_marca",store=True)

    _sql_constraints = [
        ('barcode_uniq', 'Check(1=1)', _("A barcode can only be assigned to one product !")),
    ]

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

    name= fields.Char(string="Configuración Código de Barras")
    based_on = fields.Selection([
            ('reference', _('Referencia Automática')), 
            ('default_code', _('Referencia Interna')),
        ], index=True, change_default=True, string="Basado en",
        default='reference',
        track_visibility='always',
        help="Si selecciona Referencia Automática el código de barras se llenará con la referencia automática de las variantes. De lo contrario el código de barras se llenará con la referencia interna de las variantes")
