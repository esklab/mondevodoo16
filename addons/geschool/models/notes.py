from odoo import _, api, fields, models, tools

class EcoleNotes(models.Model):
    _name = 'ecole.notes'
    _description = 'Modèle de notes'

    etudiant_id = fields.Many2one('ecole.etudiant', string='Étudiant')
    cours_id = fields.Many2one('ecole.cours', string='Cours')
    note = fields.Integer(string='Note', required=True, digits=(2, 0), 
        help="La note de l'étudiant (de 1 à 20)")
