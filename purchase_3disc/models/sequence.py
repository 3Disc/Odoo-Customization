
from odoo import models, fields, api
from odoo.addons.base.models.ir_sequence import IrSequence,_create_sequence
from datetime import datetime, timedelta

#will iterate based on when generated, so no need to consider other factors.
class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    date_previous = fields.Date(string='Last Date', default=fields.Datetime.now)
    yearly_reset = fields.Boolean(string='Yearly Reset',default=False)

    @api.model
    def create(self, values):
        """ Create a sequence, in implementation == standard a fast gaps-allowed PostgreSQL sequence is used.
        """
        self.date_previous=fields.Datetime.now
        seq = super(IrSequence, self).create(values)
        return seq

    def _next(self, sequence_date=None):

        if(self.yearly_reset):
            thisyear=datetime.now().year
            lastyear=self.date_previous.year
            if thisyear!=lastyear:
                self.date_previous = datetime.today().strftime('%Y-%m-%d')
                self.number_next_actual=1
                super(IrSequence,self)._set_number_next_actual()

        if not self.use_date_range:
            return self._next_do() 
        dt = sequence_date or self._context.get('ir_sequence_date', fields.Date.today())
        seq_date = self.env['ir.sequence.date_range'].search([('sequence_id', '=', self.id), ('date_from', '<=', dt), ('date_to', '>=', dt)], limit=1)
        if not seq_date:
            seq_date = super(IrSequence,self)._create_date_range_seq(dt)
        return seq_date.with_context(ir_sequence_date_range=seq_date.date_from)._next()