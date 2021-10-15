# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.tools.float_utils import float_compare, float_round
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.addons.purchase.models.purchase import PurchaseOrder
from odoo.addons.purchase.models.purchase import PurchaseOrderLine


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    department_id = fields.Many2one('purchase_3disc.department', string='Department', required=True)
    category_id = fields.Many2one('purchase_3disc.category', string='Category', required=True)
    department_code = fields.Char(string='Department Code')
    category_code = fields.Char(string='Category Code')

#use date when created for sequence number, reset to 1 on new year.
    @api.model
    def create(self, vals):
        company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
        department_id = vals.get('department_id',0)
        category_id = vals.get('category_id',0)
        department_list=self.env["purchase_3disc.department"]
        category_list=self.env["purchase_3disc.category"]

        department_code=str(department_list.browse(department_id).code)
        category_code=str(category_list.browse(category_id).code)
        # Ensures default picking type and currency are taken from the right company.
        self_comp = self.with_company(company_id)
        if vals.get('name', 'New') == 'New':
            seq_date = fields.Datetime.context_timestamp(self, datetime.today())
            sequence_code = self_comp.env['ir.sequence'].next_by_code('purchase_3disc.order', sequence_date=seq_date) or '/'
            sequence_code = sequence_code.replace('DPT',department_code)
            sequence_code = sequence_code.replace('CTG',category_code)
            vals['name'] = sequence_code

        res = super(PurchaseOrder, self_comp).create(vals)
        return res
    

#    @api.onchange('department_id','category_id')
#    def onchange_sequence_comp(self):
#Add code to regenerate sequence number, not sure if needed.
#        return {}

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    part_number = fields.Char(string='Part Number',store=True)
    part_description = fields.Char(string='Part Description',store=True)

    @api.model_create_multi
    def create(self, vals_list):
        super(PurchaseOrderLine, self).create(vals_list)

    @api.model
    def _prepare_add_missing_fields(self, values):
        """ Deduce missing required fields from the onchange """
        res = {}
        onchange_fields = ['name', 'price_unit', 'product_qty', 'product_uom', 'taxes_id', 'date_planned',"part_number","part_description"]
        if values.get('order_id') and values.get('product_id') and any(f not in values for f in onchange_fields):
            line = self.new(values)
            line.onchange_product_id()
            for field in onchange_fields:
                if field not in values:
                    res[field] = line._fields[field].convert_to_write(line[field], line)
        return res

    @api.onchange('product_id')
    def onchange_product_id(self):
        if not self.product_id:
            return

        # Reset date, price and quantity since _onchange_quantity will provide default values
        self.price_unit = self.product_qty = 0.0

        self._product_id_change()

        self._suggest_quantity()
        self._onchange_quantity()

        
    def _product_id_change(self):
        if not self.product_id:
            return

        self.part_number = self.product_id.barcode or self.product_id.default_code
        self.part_description = self.product_id.name

        return super(PurchaseOrderLine, self)._product_id_change()