
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


class Department(models.Model):
    _name = "purchase_3disc.department"
    _description = "Department Code"
    _order = 'sequence, id'
    _rec_name = 'name'

    name = fields.Text('Department')
    code = fields.Text('Code')
    sequence = fields.Integer('Sequence', help="Determine the display order", index=True)

    @api.model
    def create(self, vals):
        self.name = vals.get('name')
        self.code = vals.get('code')
        return super(Department,self).create(vals)

    def write(self, vals):
        """Override to make sure attribute type can't be changed if it's used on
        a product template.

        This is important to prevent because changing the type would make
        existing combinations invalid without recomputing them, and recomputing
        them might take too long and we don't want to change products without
        the user knowing about it."""
        invalidate_cache = 'sequence' in vals and any(record.sequence != vals['sequence'] for record in self)
        res = super(Department, self).write(vals)
        if invalidate_cache:
            # prefetched o2m have to be resequenced
            # (eg. product.template: attribute_line_ids)
            self.flush()
            self.invalidate_cache()
        return res
    def unlink(self):
        for pa in self:
            if pa.is_used_on_products:
                raise UserError(
                    _("You cannot delete the attribute %s because it is used on the following products:\n%s") %
                    (pa.display_name, ", ".join(pa.product_tmpl_ids.mapped('display_name')))
                )
        return super(Department, self).unlink()

class SubCategory(models.Model):
    _name = "purchase_3disc.category"
    _description = "Category Code"
    _order = 'sequence, id'
    _rec_name = 'name'

    name = fields.Text('Sub-Category', required=True)
    code = fields.Text('Code', required=True)
    sequence = fields.Integer('Sequence', help="Determine the display order", index=True)
    
    @api.model
    def create(self, vals):
        self.name = vals.get('name')
        self.code = vals.get('code')
        return super(SubCategory,self).create(vals)

    def write(self, vals):
        """Override to make sure attribute type can't be changed if it's used on
        a product template.

        This is important to prevent because changing the type would make
        existing combinations invalid without recomputing them, and recomputing
        them might take too long and we don't want to change products without
        the user knowing about it."""
        invalidate_cache = 'sequence' in vals and any(record.sequence != vals['sequence'] for record in self)
        res = super(Department, self).write(vals)
        if invalidate_cache:
            # prefetched o2m have to be resequenced
            # (eg. product.template: attribute_line_ids)
            self.flush()
            self.invalidate_cache()
        return res
    def unlink(self):
        return super(SubCategory, self).unlink()