from odoo import fields, models, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    chatter_position = fields.Selection([
        ('side', 'Side'),
        ('bottom', 'Bottom'),
    ], string='Chatter Position', default='side')

    chatter_width = fields.Integer(string='Chatter Width (px)', default=450)
    chatter_collapsed = fields.Boolean(string='Chatter Collapsed', default=False)

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ['chatter_position', 'chatter_width', 'chatter_collapsed']

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ['chatter_position', 'chatter_width', 'chatter_collapsed']
