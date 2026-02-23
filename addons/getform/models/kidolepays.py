from odoo import models, fields

class KidolePays(models.Model):
    _name = 'kidole.pays'
    
    name = fields.Char(string='Nom du Pays')
    regions = fields.One2many('kidole.region','pays_id', string='Regions')