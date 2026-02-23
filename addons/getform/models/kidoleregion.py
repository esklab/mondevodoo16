from odoo import models, fields

class KidoleRegion(models.Model):
    _name = 'kidole.region'

    name = fields.Char(string='Nom du Region')
    pays_id = fields.Many2one('kidole.pays', string='Pays')
    villes = fields.One2many('kidole.ville', 'region_id', string='Villes')