from odoo import _, api, fields, models, tools
import datetime

class EcoleEleve(models.Model):

    _name = 'ecole.eleve'
    _description = 'Eleve'

    name = fields.Char(string="Nom de l'eleve",default="JUSTIN",required=True, )
    date_naissance = fields.Datetime(string="Date de naissance",default=fields.Date.today())
    photo = fields.Binary(string="Photo de l'eleve")
    est_apt = fields.Boolean(string="Est apte pour le sport",default=True)
    age = fields.Integer(string="Age de l'eleve",compute="calcul_age")
    parent_id = fields.Many2one(
        'eleve.parent',
        string='parent',
        )
    partner_id = fields.Many2one(
        'res.partner',
        string='Client',
        )
    classe_id = fields.Many2one(
        'eleve.classe',
        string='Classe',
        )
    
    @api.depends('date_naissance')
    def calcul_age(self):
        for eleve in self:
            if eleve.date_naissance:
                today = fields.Date.context_today(eleve)
                birth_date = eleve.date_naissance.date()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                eleve.age = age


class EleveParent(models.Model):

    _name = 'eleve.parent'
    _description = 'Parent d\'eleve'

    name = fields.Char(string="Nom du Parent")
    telephone = fields.Char(string="Telephone")


class EleveClasse(models.Model):
    _name = 'eleve.classe'
    _description='Classe'

    name = fields.Char(string="Nom de la Classe")
