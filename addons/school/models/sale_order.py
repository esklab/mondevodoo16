from odoo import _, api, fields, models, tools

class SaleOrder(models.Model):

    _inherit = 'sale.order'
    mon_champ = fields.Char(string="Mon champ")

 
