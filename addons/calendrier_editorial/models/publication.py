from odoo import _, api, fields, models, tools

class CalendrierPublication(models.Model):

    _name = 'calendrier.publication'
    _description = 'Modele Publication'

    name = fields.Char(string="Publication")
    caption = fields.Char(string="Description")
    image = fields.Binary(string="Image")
    calendrier_id = fields.Many2one('calendrier.edition', string='Calendrier associé')
    status = fields.Selection([('brouillon', 'Brouillon'),
                              ('en_cours', 'En Cours'),
                              ('publié', 'Publié')],
                              default='brouillon',string='Status')
    
    show_facebook_link = fields.Boolean(string="Afficher le lien Facebook")
    facebook_link = fields.Char(string="Lien Facebook")

    show_twitter_link = fields.Boolean(string="Afficher le lien Twitter")
    twitter_link = fields.Char(string="Lien Twitter")

    show_instagram_link = fields.Boolean(string="Afficher le lien Instagram")
    instagram_link = fields.Char(string="Lien Instagram")
    
    def action_open_calendar(self):
        if self.calendrier_id:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Calendrier associé'),
                'view_mode': 'form',
                'res_model': 'calendrier.edition',
                'res_id': self.calendrier_id.id,
                'target': 'current',
            }