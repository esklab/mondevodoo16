from odoo import _,fields,models,tools 

class EcoleEtudiant(models.Model):

    _name = 'ecole.etudiant'
    _description = 'Etudiant'

    name = fields.Char(string='Nom Etudiant', required=True)
    prenom = fields.Char(string='Prénom', required=True)
    date_naissance = fields.Date(string='Date de naissance')
    adresse = fields.Text(string='Adresse')
    telephone = fields.Char(string='Numéro de téléphone')
    classe_id = fields.Many2one('ecole.classe', string='Classe')
    note_ids = fields.One2many('ecole.notes', 'etudiant_id', string='Notes')
    cours_ids = fields.Many2many('ecole.cours', 'etudiant_cours_rel', 'etudiant_id', 'cours_id', string='Cours')
    parent_id = fields.Many2one('ecole.parent',string='Parent')

