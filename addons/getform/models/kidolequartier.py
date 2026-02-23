from odoo import models, fields

class KidoleQuartier(models.Model):
    _name = 'kidole.quartier'

    name = fields.Char(string='Nom du Quartier')
    ville_id = fields.Many2one('kidole.ville', string='Ville')