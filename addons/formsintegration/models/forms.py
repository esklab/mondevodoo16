from odoo import models, fields, api
import requests

class RandomUserPartner(models.Model):
    _name = 'random.user.partner'
    _description = 'Random User Partner'

    name = fields.Char(string='Name')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')

    @api.model
    def create_random_user_partner(self):
        api_url = 'https://randomuser.me/api/?results=100'
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            data = response.json()
            user = data.get('results')[0]

            partner_vals = {
                'name': user.get('name', {}).get('first'),
                'email': user.get('email'),
                'phone': user.get('phone'),
            }

            new_partner = self.create(partner_vals)
            return {
                'name': 'Random User Created',
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'random.user.partner',
                'res_id': new_partner.id,
                'type': 'ir.actions.act_window',
            }

        except requests.RequestException as e:
            print(f"Erreur lors de la requête à l'API RandomUser.me : {str(e)}")
            return {
                'name': 'Error',
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'random.user.partner',
                'type': 'ir.actions.act_window',
            }
