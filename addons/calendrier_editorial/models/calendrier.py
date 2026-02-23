from odoo import _, api, fields, models, tools

class CalendrierEdition(models.Model):

    _name = 'calendrier.edition'
    _description = 'Modèle Calendrier'

    name = fields.Char('Nom Calendrier')
    date_debut = fields.Date(string="Date debut",required=True)
    date_fin = fields.Date(string="Date fin",required=True)

    projet_id = fields.Many2one('project.project',string='Projet')
    responsable_id = fields.Many2one('hr.employee', string='Responsable')
    montant = fields.Float(string='Montant Sponsoring')
    publication_ids = fields.One2many('calendrier.publication','calendrier_id',string="Publication")
    steps = fields.Selection([('brief', 'Brief'),
                              ('creation graphique', 'Creation Graphique'),
                              ('correction', 'Correction'),
                              ('validation', 'Validation'),
                              ('publication', 'Publication'),
                              ('achevé', 'Achevé'),],
                              default='brief',string='Etapes')
    
    @api.onchange('date_debut')
    def _onchange_start_date(self):
        if self.date_debut:
            if self.date_fin and self.date_fin < self.date_debut:
                self.date_fin = self.date_debut