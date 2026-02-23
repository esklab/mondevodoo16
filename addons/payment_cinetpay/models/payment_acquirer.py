from odoo import _, api, fields, models, tools 
from odoo.exceptions import UserError, ValidationError
import time
import requests
from hashlib import sha256

class PaymentAcquirer(models.Model):

    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('cinetpay', "Cinetpay")], ondelete={'cinetpay': 'set default'})
    cinetpay_api_key = fields.Char(string='Api key')
    cinetpay_site_id = fields.Char(string='Site ID')

    def _cinetpay_make_request(self, data = None, method="post"):
        self.ensure_one()
        endpoint_url = "https://api.cinetpay.com/v2/"
        api_key = self.cinetpay_api_key
        site_id = self.cinetpay_site_id

        headers = {
            'apikey': api_key,
            'site_id': site_id,
            'Content-Type': 'application/json',
        }        

        try:
            if method == 'post':
                response = requests.post(endpoint_url + '/payment',  headers=headers, json=data)
            else:
                response = requests.get(endpoint_url + '/payment',  headers=headers)
        except:
            raise UserError(_("Erreur lors de la connexon à l'API : Vérifiez votre connexion Internet"))

        if response.status_code != 201:
            raise UserError(_('Erreur : ' + str(response.status_code)) + ' Message : ' + response.text)
        
        return response.json()
