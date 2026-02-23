from odoo import _, api, fields, models, tools

class EcoleCours(models.Model):
    _name = 'ecole.cours'
    _description = 'Modèle de cours'

    name = fields.Char(string='Nom du cours', required=True)
    enseignant_id = fields.Many2one('ecole.enseignant', string='Enseignant')
    classe_id = fields.Many2one('ecole.classe', string='Classe associée')
