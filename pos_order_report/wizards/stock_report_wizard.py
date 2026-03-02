from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import ValidationError, UserError
from collections import defaultdict

class HospitalizationReportWizard(models.TransientModel):
    _name = 'hospitalization.report.wizard'
    _description = "Rapport d'Hospitalisation par Année/Mois"

    year = fields.Selection(
        selection=lambda self: [(str(year), str(year)) for year in range(2000, datetime.now().year + 1)],
        string="Année",
        default=str(datetime.now().year)
    )
    ward_ids = fields.Many2many('hospital.ward', string="Salles/Chambres")
    bed_ids = fields.Many2many('hospital.bed', string="Lits")
    gender = fields.Selection([
        ('male', 'Homme'),
        ('female', 'Femme'),
        ('other', 'Autres'),
    ], string="Genre")
    surgery_template_ids = fields.Many2many('hms.surgery.template', string="Actes chirurgicaux")
    outcome = fields.Selection([
        ('discharged', 'Décharge'),
        ('evaluation', 'Evaluation'),
        ('cured', 'Guérison'),
        ('death', 'Décès'),
    ], string="Mode de sortie")

    def _compute_age(self, birth_date):
        if not birth_date:
            return 0
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    def _get_hospitalization_data(self):
        domain = [('state', '=', 'done')]  # Seulement les hospitalisations terminées
        
        if self.year:
            domain.extend([
                ('hospitalization_date', '>=', f"{self.year}-01-01"),
                ('hospitalization_date', '<=', f"{self.year}-12-31")
            ])
        if self.ward_ids:
            domain.append(('ward_id', 'in', self.ward_ids.ids))
        if self.bed_ids:
            domain.append(('bed_id', 'in', self.bed_ids.ids))
        if self.gender:
            domain.append(('patient_id.gender', '=', self.gender))
        if self.surgery_template_ids:
            domain.append(('surgery_ids.template_id', 'in', self.surgery_template_ids.ids))
        if self.outcome:
            domain.append(('outcome', '=', self.outcome))

        hospitalizations = self.env['inpatient.registration'].search(domain)
        
        # Structure pour grouper par mois
        monthly_data = defaultdict(lambda: {
            'count': 0,
            'patients': [],
            'total_stay_duration': 0,
            'outcomes': defaultdict(int),
            'surgeries': defaultdict(int),
        })

        month_names = [
            'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
            'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
        ]

        for hosp in hospitalizations:
            if not hosp.hospitalization_date:
                continue
                
            month = hosp.hospitalization_date.month
            month_name = month_names[month - 1]
            
            stay_duration = 0
            if hosp.hospitalization_date and hosp.discharge_date:
                delta = hosp.discharge_date - hosp.hospitalization_date
                stay_duration = delta.days

            # Données du patient
            patient_data = {
                'name': hosp.patient_id.name,
                'age': self._compute_age(hosp.patient_id.birthday),
                'gender': dict(hosp.patient_id._fields['gender'].selection).get(hosp.patient_id.gender),
                'surgery': ", ".join(hosp.surgery_ids.mapped('template_id.name')),
                'diagnosis': ", ".join(hosp.diseases_ids.mapped('name')),
                'operating_block': hosp.hospital_it_id.name if hosp.hospital_it_id else '',
                'stay_duration': stay_duration,
                'outcome': dict(self._fields['outcome'].selection).get(hosp.outcome) if hosp.outcome else '',
                'ward': hosp.ward_id.name if hosp.ward_id else '',
                'bed': hosp.bed_id.name if hosp.bed_id else '',
                'spo2': hosp.spo2,
            }

            # Mise à jour des statistiques mensuelles
            monthly_data[month_name]['count'] += 1
            monthly_data[month_name]['patients'].append(patient_data)
            monthly_data[month_name]['total_stay_duration'] += stay_duration
            
            if hosp.outcome:
                monthly_data[month_name]['outcomes'][hosp.outcome] += 1
            
            for surgery in hosp.surgery_ids:
                monthly_data[month_name]['surgeries'][surgery.template_id.name] += 1

        # Convertir le defaultdict en dict ordonné par mois
        sorted_data = []
        for month in month_names:
            if month in monthly_data:
                sorted_data.append({
                    'month': month,
                    'data': monthly_data[month]
                })

        return {
            'year': self.year,
            'monthly_data': sorted_data,
            'total_hospitalizations': len(hospitalizations),
        }

    def action_generate_report(self):
        data = self._get_hospitalization_data()
        if not data['monthly_data']:
            raise UserError(_("Aucune donnée trouvée avec les critères sélectionnés"))
        
        return self.env.ref('your_module.report_hospitalization_monthly_action').report_action(self, data=data)