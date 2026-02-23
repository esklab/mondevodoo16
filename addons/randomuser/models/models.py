from odoo import models, fields, api
import requests

class RandomUser(models.Model):
    _name = 'random.user'
    _description = 'Random User Data'

    name = fields.Char('Nom')
    email = fields.Char('Email')
    phone = fields.Char('Téléphone')

    @api.model
    def get_random_user_data(self):
        api_url = "https://randomuser.me/api/?results=1"  
        data = response.json().get('results')[0] 

        random_user = self.create({
            'name': f"{data['name']['first']} {data['name']['last']}",
            'email': data['email'],
            'phone': data['phone'],
        })

        return random_user

    def action_fetch_random_user(self):
        random_user = self.get_random_user_data()
        return {
            'name': "Détails de l'utilisateur aléatoire",
            'view_mode': 'form',
            'res_model': 'random.user',
            'res_id': random_user.id,
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref('randomuser.view_random_user_form').id,
            'target': 'current',
        }
