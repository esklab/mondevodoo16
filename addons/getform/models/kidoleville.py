from odoo import models, fields

class KidoleVille(models.Model):
    _name = 'kidole.ville'

    name = fields.Char(string='Nom de la Ville')
    region_id = fields.Many2one('kidole.region', string='Region')
    quartiers = fields.One2many('kidole.quartier', 'ville_id', string='Quartiers')