from odoo import fields, models


class HcPractitioner(models.Model):
    _name = "hc.practitioner"
    _description = "Healthcare Practitioner"
    _order = "name"

    name = fields.Char(required=True)
    practice_id = fields.Many2one(
        "hc.practice",
        string="Practice",
        required=True,
        default=lambda self: self.env.user.practice_id,
        help="Practice this practitioner belongs to.",
    )
    active = fields.Boolean(default=True)
