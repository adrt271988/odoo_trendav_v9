# -*- coding: utf-8 -*-
import logging
import psycopg2
import time
from datetime import datetime
import uuid
import sets

from functools import partial

import openerp
import openerp.addons.decimal_precision as dp
from openerp import tools, models, SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools import float_is_zero
from openerp.tools.translate import _
from openerp.exceptions import UserError

from openerp import api, fields as Fields

_logger = logging.getLogger(__name__)

class trend_pos_session(osv.osv):
    _inherit = "pos.session"

    def _get_st_line(self, cr, uid, ids, field_names, arg=None, context=None):
        result = dict((res_id, []) for res_id in ids)
        for session in self.browse(cr, uid, ids, context=context):
            for st in session.statement_ids:
                result[session.id] += [st_line.id for st_line in st.line_ids]
        return result

    _columns = {
        'statement_lines': fields.function(_get_st_line, method=True, type='one2many', relation='account.bank.statement.line', string='Pagos y Extractos Bancarios'),
    }

class trend_pos_order(osv.osv):
    _inherit = "pos.order"

    def _process_order(self, cr, uid, order, context=None):
        prec_acc = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
        session = self.pool.get('pos.session').browse(cr, uid, order['pos_session_id'], context=context)

        if session.state == 'closing_control' or session.state == 'closed':
            session_id = self._get_valid_session(cr, uid, order, context=context)
            session = self.pool.get('pos.session').browse(cr, uid, session_id, context=context)
            order['pos_session_id'] = session_id

        order_id = self.create(cr, uid, self._order_fields(cr, uid, order, context=context),context)
        journal_ids = set()
        for payments in order['statement_ids']:
            if not float_is_zero(payments[2]['amount'], precision_digits=prec_acc):
                self.add_payment(cr, uid, order_id, self._payment_fields(cr, uid, payments[2], context=context), context=context)
            journal_ids.add(payments[2]['journal_id'])

        if session.sequence_number <= order['sequence_number']:
            session.write({'sequence_number': order['sequence_number'] + 1})
            session.refresh()

        if order['amount_paid'] != 0 and order['amount_total'] < order['amount_paid'] and not float_is_zero(order['amount_return'], precision_digits=prec_acc):
            cash_journal = session.cash_journal_id.id
            if not cash_journal:
                # Select for change one of the cash journals used in this payment
                cash_journal_ids = self.pool['account.journal'].search(cr, uid, [
                    ('type', '=', 'cash'),
                    ('id', 'in', list(journal_ids)),
                ], limit=1, context=context)
                if not cash_journal_ids:
                    # If none, select for change one of the cash journals of the POS
                    # This is used for example when a customer pays by credit card
                    # an amount higher than total amount of the order and gets cash back
                    cash_journal_ids = [statement.journal_id.id for statement in session.statement_ids
                                        if statement.journal_id.type == 'cash']
                    if not cash_journal_ids:
                        raise UserError(_("No cash statement found for this session. Unable to record returned cash."))
                cash_journal = cash_journal_ids[0]
            self.add_payment(cr, uid, order_id, {
                'amount': -order['amount_return'],
                'payment_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'payment_name': _('return'),
                'journal': cash_journal,
            }, context=context)

        #Para devolver con otra forma de pago distinta diario de efectivo
        if order['amount_paid'] == 0.0 and not float_is_zero(order['amount_return'], precision_digits=prec_acc):
            for payments in order['statement_ids']:
                self.add_payment(cr, uid, order_id, {
                    'amount': -order['amount_return'],
                    'payment_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'payment_name': _('Devolución'),
                    'journal': payments[2]['journal_id'],
                }, context=context)
        return order_id
