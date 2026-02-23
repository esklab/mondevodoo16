from odoo import models, fields, api

class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave'
    holiday_type = fields.Selection(string='Allocation Mode', selection=[('employee', 'By Employee'), ('company', 'By Company')],default='employee')
    number_of_days_display = fields.Float()

    @api.model
    def create(self, values):
        rec = super(HrLeaveAllocation, self).create(values)
        if rec.employee_id.weekly_hours:
            # Get the actual hours worked by the employee from the planning module
            actual_hours = self.env['planning.slot'].search([('employee_id', '=', rec.employee_id.id), ('start_date', '>=', start_of_week), ('end_date', '<=', end_of_week)]).mapped('allocated_hours')
            if actual_hours > rec.employee_id.weekly_hours:
                extra_hours = actual_hours - rec.employee_id.weekly_hours
                extra_days = extra_hours / 8  # Convert hours to days
                rec.write({'number_of_days_display': rec.number_of_days_display + extra_days})
            elif actual_hours < rec.employee_id.weekly_hours:
                missing_hours = rec.employee_id.weekly_hours - actual_hours
                missing_days = missing_hours / 8  # Convert hours to days
                rec.write({'number_of_days_display': rec.number_of_days_display - missing_days})
        return rec
