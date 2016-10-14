# -*- coding: utf-8 -*-

from openerp import tools
from openerp.osv import fields,osv

class report_trend_pos_order(osv.osv):
    _name = "report.trend.pos.order"
    _description = "Estadísticas TPV Trend"
    _auto = False

    _columns = {
        'date': fields.datetime('Fecha Pedido', readonly=True),
        'partner_id':fields.many2one('res.partner', 'Cliente', readonly=True),
        'product_id':fields.many2one('product.product', 'Producto', readonly=True),
        'product_tmpl_id': fields.many2one('product.template', 'Product Plantilla', readonly=True),
        'state': fields.selection([('draft', 'Nuevo'), ('paid', 'Pagado'), ('done', 'Contabilizado'), ('invoiced', 'Facturado'), ('cancel', 'Cancelado')],
                                  'Estado'),
        'user_id':fields.many2one('res.users', 'Vendedor', readonly=True),
        'price_total':fields.float('Precio Total', readonly=True),
        'price_sub_total':fields.float('Subtotal sin descuento', readonly=True),
        'total_discount':fields.float('Descuento Total', readonly=True),
        'average_price': fields.float('Precio Promedio', readonly=True,group_operator="avg"),
        'location_id':fields.many2one('stock.location', 'Ubicación', readonly=True),
        'company_id':fields.many2one('res.company', 'Compañía', readonly=True),
        'nbr':fields.integer('# de Líneas', readonly=True),  # TDE FIXME master: rename into nbr_lines
        'product_qty':fields.integer('Cantidad de Producto', readonly=True),
        'journal_id': fields.many2one('account.journal', 'Diario'),
        'delay_validation': fields.integer('Validación de retardo'),
        'product_categ_id': fields.many2one('product.category', 'Categoría de Producto', readonly=True),
        'invoiced': fields.boolean('Facturado', readonly=True),
        'config_id' : fields.many2one('pos.config', 'Punto de Venta', readonly=True),
        'pos_categ_id': fields.many2one('pos.category','Categoría Pública', readonly=True),
        'stock_location_id': fields.many2one('stock.location', 'Almacén', readonly=True),
        'pricelist_id': fields.many2one('product.pricelist', 'Lista de Precio', readonly=True),
        'marca_id': fields.many2one('product.marca','Marca',readonly=True),
        'parent_id': fields.many2one('pos.category','Categoría Padre',readonly=True),
    }
    _order = 'date desc'

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_trend_pos_order')
        cr.execute("""
            create or replace view report_trend_pos_order as (
                select
                    min(l.id) as id,
                    count(*) as nbr,
                    s.date_order as date,
                    sum(l.qty * u.factor) as product_qty,
                    sum(l.qty * l.price_unit) as price_sub_total,
                    sum((l.qty * l.price_unit) * (100 - l.discount) / 100) as price_total,
                    sum((l.qty * l.price_unit) * (l.discount / 100)) as total_discount,
                    (sum(l.qty*l.price_unit)/sum(l.qty * u.factor))::decimal as average_price,
                    sum(cast(to_char(date_trunc('day',s.date_order) - date_trunc('day',s.create_date),'DD') as int)) as delay_validation,
                    s.partner_id as partner_id,
                    s.state as state,
                    s.user_id as user_id,
                    s.location_id as location_id,
                    s.company_id as company_id,
                    s.sale_journal as journal_id,
                    l.product_id as product_id,
                    pt.categ_id as product_categ_id,
                    pt.marca_id as marca_id,
                    p.product_tmpl_id,
                    ps.config_id,
                    pt.pos_categ_id,
                    pc.stock_location_id,
                    s.pricelist_id,
                    pos_c.parent_id,
                    s.invoice_id IS NOT NULL AS invoiced
                from pos_order_line as l
                    left join pos_order s on (s.id=l.order_id)
                    left join product_product p on (l.product_id=p.id)
                    left join product_template pt on (p.product_tmpl_id=pt.id)
                    left join product_uom u on (u.id=pt.uom_id)
                    left join pos_session ps on (s.session_id=ps.id)
                    left join pos_config pc on (ps.config_id=pc.id)
                    left join pos_category pos_c on (pt.pos_categ_id = pos_c.id)
                group by
                    s.date_order, s.partner_id,s.state, pt.categ_id,
                    s.user_id,s.location_id,s.company_id,s.sale_journal,s.pricelist_id,s.invoice_id,l.product_id,s.create_date,pt.categ_id,pt.pos_categ_id,p.product_tmpl_id,ps.config_id,pc.stock_location_id,pt.marca_id,pos_c.parent_id
                having
                    sum(l.qty * u.factor) != 0)""")
