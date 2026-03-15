from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class HcCheckoutSession(models.Model):
    _inherit = "hc.checkout.session"

    service_fee_practice_id = fields.Many2one(
        "hc.practice",
        string="Service Fee Practice",
        related="appointment_id.practice_id",
        readonly=True,
    )
    service_fee_id = fields.Many2one(
        "hc.service.fee",
        string="Service Fee",
    )

    def _service_fee_default_vals(self, service_fee):
        return {
            "service_fee_id": service_fee.id,
            "charge_label": service_fee.name,
            "amount_total": service_fee.default_price,
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            appointment_id = vals.get("appointment_id")
            if not appointment_id or vals.get("service_fee_id"):
                continue
            appointment = self.env["hc.appointment"].browse(appointment_id)
            service_fee = appointment.appointment_type_id.default_service_fee_id
            if service_fee:
                vals.setdefault("service_fee_id", service_fee.id)
                vals.setdefault("charge_label", service_fee.name)
                vals.setdefault("amount_total", service_fee.default_price)
        return super().create(vals_list)

    def write(self, vals):
        if self.env.context.get("skip_session_service_fee_apply") or "service_fee_id" not in vals:
            return super().write(vals)

        if "service_fee_id" in vals:
            if any(record.state != "open" for record in self):
                raise UserError("Service fee can only be changed while checkout is open.")
            service_fee_id = vals.get("service_fee_id")
            explicit_description = vals.pop("charge_label", None) if "charge_label" in vals else None
            explicit_amount = vals.pop("amount_total", None) if "amount_total" in vals else None
            result = super().write(vals)
            for record in self:
                record._create_default_line_if_missing()
                line = record.checkout_line_ids.sorted(key=lambda item: (item.sequence, item.id))[:1]
                if not line:
                    continue
                line_vals = {}
                if service_fee_id:
                    service_fee = self.env["hc.service.fee"].browse(service_fee_id)
                    line_vals.update(
                        {
                            "service_fee_id": service_fee.id,
                            "description": service_fee.name,
                            "amount": service_fee.default_price,
                        }
                    )
                else:
                    line_vals["service_fee_id"] = False
                if explicit_description is not None:
                    line_vals["description"] = explicit_description
                if explicit_amount is not None:
                    line_vals["amount"] = explicit_amount
                line.with_context(skip_session_service_fee_apply=True).write(line_vals)
            return result
        return super().write(vals)

    @api.onchange("service_fee_id")
    def _onchange_service_fee_id(self):
        if self.state != "open" or not self.service_fee_id:
            return
        self.charge_label = self.service_fee_id.name
        self.amount_total = self.service_fee_id.default_price
