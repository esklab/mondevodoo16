from odoo import models, fields, api
import requests
import json

class JetForm(models.Model):
    _name = 'jet.form'
    _description = 'Jet Form Data'
    
    name = fields.Char('Nom')
    email = fields.Char('Email')
    phone = fields.Char('Téléphone')
    address = fields.Char('Adresse')

    @api.model
    def get_jetform_data(self):
        api_url = "https://api.jotform.com/form/233203591543552/submissions?apiKey=a3420bff38d145c820e365099f2e1dd2"
        response = requests.get(api_url)
        response.raise_for_status()  # Lève une exception en cas d'erreur HTTP
        data = response.json().get('content', [])

        for submission in data:
            # Vérifier si les données du formulaire ne sont pas vides
            if submission.get('answers'):
                full_name = f"{submission['answers']['3']['prettyFormat']}"
                email = submission['answers']['5']['answer']
                phone = submission['answers']['4']['prettyFormat']
                address = submission['answers']['6']['answer'].get('addr_line1', '')

                # Créer un enregistrement dans le modèle Odoo pour chaque soumission
                jetform = self.create({
                    'name': full_name,
                    'email': email,
                    'phone': phone,
                    'address': address,
                })
        return True

    def action_fetch_jetform(self):
        self.get_jetform_data()
        return {
            'name': 'Détails de l\'utilisateur aléatoire',
            'view_mode': 'tree,form',
            'res_model': 'jet.form',
            'type': 'ir.actions.act_window',
            'domain': [],
            'view_id': False,
            'target': 'new',
            "context":{},
        }