from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HcServiceFee(models.Model):
    _name = "hc.service.fee"
    _description = "Healthcare Service Fee"
    _order = "name, id"

    name = fields.Char(required=True)
    practice_id = fields.Many2one(
        "hc.practice",
        string="Practice",
        required=True,
        default=lambda self: self.env.user.practice_id,
    )
    active = fields.Boolean(default=True)
    default_price = fields.Monetary(
        string="Default Price",
        required=True,
        default=0.0,
        currency_field="currency_id",
    )
    short_description = fields.Char(string="Short Description")
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    @api.constrains("default_price")
    def _check_default_price(self):
        for record in self:
            if record.default_price < 0:
                raise ValidationError("Service fee default price must be zero or greater.")
