from odoo import fields, models


class HcPractice(models.Model):
    _name = "hc.practice"
    _description = "Healthcare Practice"
    _order = "name"

    name = fields.Char(required=True)
    timezone = fields.Char(
        default=lambda self: self.env.user.tz or "UTC",
        help="Default timezone for this practice.",
    )
    active = fields.Boolean(default=True)

