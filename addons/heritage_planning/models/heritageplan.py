from odoo import api, fields, models
from datetime import datetime, timedelta, time
from pytz import timezone

import logging

_logger = logging.getLogger(__name__)

class HrLeaveAllocationExtended(models.Model):
    _inherit = 'hr.leave.allocation'

    number_of_days = fields.Float(string='Number of Days', readonly=False)
    number_of_days_display = fields.Float(string='Duration (days)', readonly=False)
    is_negative_allocation = fields.Boolean(
        string='Is Negative Allocation', 
        default=False,
        help="Indicates if this allocation represents a deduction for insufficient hours"
    )

class PlanningSlot(models.Model):
    _inherit = 'planning.slot'

    def get_employees_with_allocated_hours(self):
        """Return employees with allocated hours in current week"""
        start_date, end_date = self.get_week_boundaries()
        _logger.info(f"Recherche des employés avec heures allouées entre {start_date} et {end_date}")
        
        slots = self.search([
            ('allocated_hours', '>', 0),
            ('start_datetime', '>=', start_date),
            ('end_datetime', '<=', end_date)
        ])
        
        employees = slots.mapped('employee_id')
        _logger.info(f"Nombre d'employés trouvés avec heures allouées: {len(employees)}")
        return employees

    def get_week_boundaries(self):
        """Return timezone-aware week boundaries"""
        tz = self.env.user.tz or 'UTC'
        tz = timezone(tz)
        now = fields.Datetime.now().astimezone(tz)
    
        # Début de semaine (lundi 00:00:00)
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = tz.localize(
            datetime.combine(start_of_week.date(), time.min)
        )
    
        # Fin de semaine (dimanche 23:59:59.999999)
        end_of_week = start_of_week + timedelta(days=6)
        end_of_week = tz.localize(
            datetime.combine(end_of_week.date(), time.max)
        )
    
        return start_of_week, end_of_week

    def get_allocated_hours_for_employee(self, employee, start_date, end_date):
        """Return allocated hours for employee in date range"""
        _logger.debug(f"Recherche des heures allouées pour {employee.name} entre {start_date} et {end_date}")
        
        slots = self.search([
            ('employee_id', '=', employee.id),
            ('start_datetime', '>=', start_date),
            ('end_datetime', '<=', end_date),
            ('allocated_hours', '>', 0),
        ])
        
        hours = slots.mapped('allocated_hours')
        _logger.debug(f"Heures allouées trouvées pour {employee.name}: {hours}")
        return hours

    def get_weekly_hours(self, calendar):
        """Calculate weekly working hours based on calendar attendance"""
        if not calendar:
            _logger.warning(f"Aucun calendrier trouvé, utilisation de la valeur par défaut 40h")
            return 40.0
        
        total = 0.0
        for day in calendar.attendance_ids:
            total += (day.hour_to - day.hour_from)
        
        _logger.debug(f"Heures hebdomadaires calculées pour le calendrier {calendar.name}: {total}h")
        return total

    def calculate_difference_hours(self, employee):
        """Calculate difference between allocated hours and employee's weekly working hours"""
        _logger.info(f"Calcul de la différence d'heures pour {employee.name}")
        
        weekly_hours = self.get_weekly_hours(employee.resource_calendar_id)
        start_date, end_date = self.get_week_boundaries()
        allocated_hours = sum(self.get_allocated_hours_for_employee(employee, start_date, end_date))
        
        if not allocated_hours:
            _logger.info(f"Aucune heure allouée trouvée pour {employee.name} - non concerné")
            return 0.0
            
        difference = allocated_hours - weekly_hours
        _logger.info(f"Différence calculée pour {employee.name}: {difference}h (Alloué: {allocated_hours}h, Contractuel: {weekly_hours}h)")
        return difference

    def create_leave_allocation(self, employee, difference_hours):
        """Create leave allocation record based on hours difference"""
        if difference_hours == 0:
            _logger.debug(f"Aucune allocation à créer pour {employee.name} (différence: 0)")
            return False
            
        allocation_type = "positives" if difference_hours > 0 else "négatives"
        _logger.info(f"Création d'allocation {allocation_type} pour {employee.name}: {abs(difference_hours)}h")
        
        allocation_vals = {
            'name': 'Heures supplémentaires' if difference_hours > 0 else 'Déduction heures manquantes',
            'holiday_status_id': 7,
            'allocation_type': 'regular',
            'number_of_days': abs(difference_hours) / 8,
            'number_of_hours_display': abs(difference_hours),
            'holiday_type': 'employee',
            'employee_id': employee.id,
            'is_negative_allocation': difference_hours < 0,
        }
        
        try:
            allocation = self.env['hr.leave.allocation'].create(allocation_vals)
            _logger.info(f"Allocation créée avec succès pour {employee.name} (ID: {allocation.id})")
            return allocation
        except Exception as e:
            _logger.error(f"Erreur lors de la création de l'allocation pour {employee.name}: {str(e)}")
            return False

    def process_leave_allocations(self):
        """Main method to process weekly leave allocations"""
        _logger.info("=== Début du traitement des allocations de congés ===")
        
        employees = self.get_employees_with_allocated_hours()
        _logger.info(f"Nombre total d'employés à traiter: {len(employees)}")
        
        for employee in employees:
            try:
                _logger.info(f"Traitement de l'employé: {employee.name} (ID: {employee.id})")
                difference_hours = self.calculate_difference_hours(employee)
                
                if difference_hours != 0:
                    leave_allocation = self.create_leave_allocation(employee, difference_hours)
                    if leave_allocation:
                        _logger.info(f"Allocation finalisée pour {employee.name}: {leave_allocation.number_of_days} jours")
                else:
                    _logger.info(f"Aucune action nécessaire pour {employee.name}")
            except Exception as e:
                _logger.error(f"Erreur lors du traitement de {employee.name}: {str(e)}")
                continue
                
        _logger.info("=== Fin du traitement des allocations de congés ===")

    def create_leave_allocation_for_all_employees(self):
        """Monthly allocation method for all employees"""
        _logger.info("=== Début de l'allocation mensuelle pour tous les employés ===")
        
        all_employees = self.env['hr.employee'].search([])
        _logger.info(f"Nombre total d'employés: {len(all_employees)}")
        
        for employee in all_employees:
            try:
                _logger.debug(f"Vérification de l'employé: {employee.name}")
                start_date, end_date = self.get_week_boundaries()
                allocated_hours = sum(self.get_allocated_hours_for_employee(employee, start_date, end_date))
                
                if allocated_hours > 0:
                    _logger.info(f"Création d'allocation mensuelle pour {employee.name}")
                    leave_allocation = self.create_leave_allocation(employee, 2.5)
                    if leave_allocation:
                        _logger.info(f"Allocation mensuelle créée pour {employee.name} (ID: {leave_allocation.id})")
                else:
                    _logger.debug(f"{employee.name} n'a pas d'heures allouées - ignoré")
            except Exception as e:
                _logger.error(f"Erreur lors du traitement mensuel de {employee.name}: {str(e)}")
                continue
                
        _logger.info("=== Fin de l'allocation mensuelle ===")

class ModuleNameInit(models.Model):
    _name = 'module.name.init'
    _description = 'Initialize module cron jobs'
    
    @api.model
    def _create_cron_jobs(self):
        """Create scheduled actions for the module"""
        _logger.info("Initialisation des cron jobs")
        
        # Weekly cron (every Sunday at 23:59)
        next_sunday = datetime.now() + timedelta(
            days=(6 - datetime.now().weekday()) % 7,
            hours=23, minutes=59, seconds=0
        )
        
        if not self.env['ir.cron'].search([('name', '=', 'Process Leave Allocations by excess time')]):
            weekly_cron = self.env['ir.cron'].create({
                'name': 'Process Leave Allocations by excess time',
                'interval_type': 'weeks',
                'interval_number': 1,
                'nextcall': next_sunday.strftime('%Y-%m-%d %H:%M:%S'),
                'model_id': self.env.ref('planning.model_planning_slot').id,
                'code': 'model.process_leave_allocations()',
                'numbercall': -1,
                'user_id': self.env.user.id,
                'priority': 5,
            })
            _logger.info(f"Cron job hebdomadaire créé (ID: {weekly_cron.id})")

        # Monthly cron (30th at 23:59)
        if not self.env['ir.cron'].search([('name', '=', 'Process Leave Allocation For All Employees')]):
            monthly_cron = self.env['ir.cron'].create({
                'name': 'Process Leave Allocation For All Employees',
                'interval_type': 'months',
                'interval_number': 1,
                'nextcall': fields.Datetime.now().replace(
                    day=30, hour=23, minute=59, second=0, microsecond=0
                ),
                'model_id': self.env.ref('planning.model_planning_slot').id,
                'code': 'model.create_leave_allocation_for_all_employees()',
                'numbercall': -1,
                'user_id': self.env.user.id,
                'priority': 5,
            })
            _logger.info(f"Cron job mensuel créé (ID: {monthly_cron.id})")

    @api.model
    def init(self):
        """Initialize module"""
        _logger.info("=== Initialisation du module ===")
        try:
            self._create_cron_jobs()
            _logger.info("Initialisation terminée avec succès")
        except Exception as e:
            _logger.error(f"Erreur lors de l'initialisation: {str(e)}")
            raise