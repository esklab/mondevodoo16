from odoo import _, api, fields, models, tools 
from odoo.exceptions import UserError, ValidationError
import time
import re
import requests
from hashlib import sha256

class PaymentAcquirer(models.Model):

    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('cashpay', "Cashpay")], ondelete={'cashpay': 'set default'})
    cashpay_api_login = fields.Char(string='Api login')
    cashpay_api_key = fields.Char(string='Api key')
    cashpay_api_refenrence = fields.Char(string='Api reference')

    def _cashapy_make_request(self, salt, data = None, method="post"):
        self.ensure_one()
        endpoint_url = "https://api.semoa-payments.ovh/prod"
        if self.state == 'test':
            endpoint_url = "https://sandbox.semoa-payments.com/api"
        else:
            endpoint_url = "https://api.semoa-payments.ovh/prod"
        login = self.cashpay_api_login
        apireference = self.cashpay_api_refenrence
        api_key = self.cashpay_api_key
        token = login + api_key + salt
        api_secure = sha256(token.encode('utf-8')).hexdigest()

        headers = {
            'login': login,
            'apisecure': api_secure,
            'apireference': apireference,
            'salt': salt,
            'Content-Type': 'application/json',
        }        
    

        response = requests.post(endpoint_url + '/orders',  headers=headers, json=data)

        if response.status_code != 201:
            raise UserError(_('Erreur : ' + str(response.status_code)) + ', Message : ' + response.text)
        
        return response.json()
    
    def cashpay_get_form_action_url(self):
        bill_url = self.bill_url
        original_url = self.get_original_url(bill_url)

        return original_url

    def get_original_url(self, short_url):
        session = requests.Session()  # so connections are recycled
        resp = session.head(short_url, allow_redirects=True)
        return resp.url
