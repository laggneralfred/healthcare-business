from odoo import fields, models


class HcConsentTemplate(models.Model):
    _name = "hc.consent.template"
    _description = "Healthcare Consent Template"
    _order = "name, id"

    name = fields.Char(required=True)
    practice_id = fields.Many2one(
        "hc.practice",
        string="Practice",
        required=True,
        default=lambda self: self.env.user.practice_id,
    )
    active = fields.Boolean(default=True)
