from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HcAppointmentType(models.Model):
    _inherit = "hc.appointment.type"

    default_service_fee_id = fields.Many2one(
        "hc.service.fee",
        string="Default Service Fee",
    )

    @api.constrains("default_service_fee_id", "practice_id")
    def _check_default_service_fee_practice(self):
        for record in self:
            if (
                record.default_service_fee_id
                and record.default_service_fee_id.practice_id != record.practice_id
            ):
                raise ValidationError(
                    "Default service fee must belong to the same practice as the appointment type."
                )
