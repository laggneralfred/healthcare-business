from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HcCheckoutLine(models.Model):
    _inherit = "hc.checkout.line"

    service_fee_practice_id = fields.Many2one(
        "hc.practice",
        string="Service Fee Practice",
        related="checkout_session_id.appointment_id.practice_id",
        readonly=True,
    )
    service_fee_id = fields.Many2one(
        "hc.service.fee",
        string="Service Fee",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            service_fee_id = vals.get("service_fee_id")
            if service_fee_id:
                service_fee = self.env["hc.service.fee"].browse(service_fee_id)
                vals.setdefault("description", service_fee.name)
                vals.setdefault("amount", service_fee.default_price)
        return super().create(vals_list)

    def write(self, vals):
        if "service_fee_id" in vals and not self.env.context.get("skip_line_service_fee_apply"):
            service_fee_id = vals.get("service_fee_id")
            if service_fee_id:
                service_fee = self.env["hc.service.fee"].browse(service_fee_id)
                vals.setdefault("description", service_fee.name)
                vals.setdefault("amount", service_fee.default_price)
        return super().write(vals)

    @api.onchange("service_fee_id")
    def _onchange_service_fee_id(self):
        if not self.service_fee_id:
            return
        self.description = self.service_fee_id.name
        self.amount = self.service_fee_id.default_price

    @api.constrains("service_fee_id", "checkout_session_id")
    def _check_service_fee_practice(self):
        for record in self:
            if (
                record.service_fee_id
                and record.checkout_session_id
                and record.service_fee_id.practice_id
                != record.checkout_session_id.appointment_id.practice_id
            ):
                raise ValidationError(
                    "Service fee must belong to the same practice as the appointment."
                )
