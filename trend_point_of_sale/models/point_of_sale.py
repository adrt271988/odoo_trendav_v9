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
