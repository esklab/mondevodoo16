from odoo import _, api, fields, models
import time
import random

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'cinetpay':
            return res
        api_data = self._get_api_bill_data()
        return {
            'api_url': api_data.get('bill_url'),
            'order_reference': api_data.get('order_reference'),
            'reference': self.reference,
        }

    def _get_api_bill_data(self):
        base_url = self.provider_id.get_base_url()
        salt = str(time.time())
        data = {
            "transaction_id": str(random.randint(10000000, 99999999)),
            'amount': int(self.amount),
            'currency': 'XOF',
            'channels': 'ALL',
            'description': 'Paiement de la facture N°' + self.reference,
            "customer_name": self.partner_id.name,
            "customer_surname": self.partner_id.name,
            "customer_email": self.partner_id.email,
            "customer_phone_number": self.partner_id.phone or '+22892416645',
            "customer_address": self.partner_id.street,
            "customer_city": self.partner_id.city,
            "customer_country": self.partner_id.country_id.code,
            "customer_state": self.partner_id.state_id.code,
            "customer_zip_code": self.partner_id.zip,
        }
        
        response = self.provider_id._cinetpay_make_request(salt, data)

        return {
            'bill_url': response.get('bill_url'),
            'order_reference': response.get('order_reference'),
        }

    @api.model
    def _get_tx_from_feedback_data(self, provider, data):
        tx = super()._get_tx_from_feedback_data(provider, data)
        if provider != 'cinetpay':
            return tx

        reference = data.get('reference')
        return self.search([('reference', '=', reference), ('provider_code', '=', 'cinetpay')])

    def _process_feedback_data(self, data):
        self.ensure_one()
        super()._process_feedback_data(data)
        if self.provider_code != "cinetpay":
            return