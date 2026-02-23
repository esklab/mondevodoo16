from odoo import _, api, fields, models, tools

class EcoleEnseignant(models.Model):
    _name = 'ecole.enseignant'
    _description = "Modèle d'enseignant"

    name = fields.Char(string='Nom Enseignant', required=True)
    prenom = fields.Char(string='Prénom', required=True)
    cours_ids = fields.Many2many('ecole.cours', string='Cours enseignés')
   