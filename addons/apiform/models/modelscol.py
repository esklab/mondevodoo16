from odoo import models, fields, api
import requests
import json

class MyModelInherited(models.Model):
    _inherit = 'ir.model.fields' 
    api_data_mapping = fields.Text(string="API Data Mapping", help="JSON data for API mapping")

    @api.model
    def map_api_data_to_odoo_fields(self, api_data):
        # Charger le mapping JSON depuis le champ api_data_mapping
        mapping_json = json.loads(self.api_data_mapping)

        # Mapper les champs API aux champs Odoo
        mapped_data = {}
        for odoo_field, api_field in mapping_json.items():
            mapped_data[odoo_field] = api_data.get(api_field, '')

        return mapped_data