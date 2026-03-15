from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    is_hc_provider = fields.Boolean(
        string="Healthcare Provider",
        default=False,
        help="Marks this internal user as a provider for Sprint 1 scheduling.",
    )

