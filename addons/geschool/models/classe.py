from odoo import _, api, fields, models, tools

class EcoleClasse(models.Model):
    _name = 'ecole.classe'
    _description = 'Modèle de classe'

    name = fields.Selection([
        ('CP1', 'CP1'),
        ('CP2', 'CP2'),
        ('CE1', 'CE1'),
        ('CE2', 'CE2'),
        ('CM1', 'CM1'),
        ('CM2', 'CM2'),
        ('6eme', '6ème'),
        ('5eme', '5ème'),
        ('4eme', '4ème'),
        ('3eme', '3ème'),
        ('2nde', '2nde'),
        ('1ere', '1ère'),
        ('Terminal', 'Terminal')],
        string='Niveau', required=True)
    
    filiere = fields.Selection([
        ('Scientifique', 'Scientifique'),
        ('Littéraire', 'Littéraire'),
        ('Technique', 'Technique'),
        ('Autre', 'Autre')],
        string='Filière')
    
    etudiant_ids = fields.Many2many('ecole.etudiant', string='Etudiants')