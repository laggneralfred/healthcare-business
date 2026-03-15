from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    practice_id = fields.Many2one(
        "hc.practice",
        string="Practice",
        help="Primary practice for this internal user.",
    )

