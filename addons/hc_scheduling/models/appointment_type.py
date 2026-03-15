from odoo import fields, models


class HcAppointmentType(models.Model):
    _name = "hc.appointment.type"
    _description = "Healthcare Appointment Type"
    _order = "name"

    name = fields.Char(required=True)
    practice_id = fields.Many2one(
        "hc.practice",
        string="Practice",
        required=True,
        default=lambda self: self.env.user.practice_id,
        help="Practice that uses this appointment type.",
    )
    active = fields.Boolean(default=True)
