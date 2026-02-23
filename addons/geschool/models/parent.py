from odoo import _, api, fields, models, tools

class EcoleParent(models.Model):
    _name = 'ecole.parent'
    _description = 'Modèle de parent d\'élève'

    name = fields.Char(string='Nom', required=True)
    adresse = fields.Text(string='Adresse')
    telephone = fields.Char(string='Numéro de téléphone')
    email = fields.Char(string='Adresse e-mail')
    etudiant_ids = fields.One2many('ecole.etudiant', 'parent_id',string='Etudiant Associé')