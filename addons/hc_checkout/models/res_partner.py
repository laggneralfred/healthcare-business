from odoo import models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_payment_due_checkout_sessions(self):
        self.ensure_one()
        return self.env["hc.checkout.session"].search(
            [
                ("patient_id", "=", self.id),
                ("state", "=", "payment_due"),
            ],
            order="appointment_start, id",
        )

    def _get_payment_due_total(self):
        self.ensure_one()
        return sum(self._get_payment_due_checkout_sessions().mapped("amount_total"))

    def _get_patient_statement_practice(self):
        self.ensure_one()
        sessions = self._get_payment_due_checkout_sessions()
        return self.practice_id or sessions[:1].appointment_id.practice_id

    def action_print_patient_statement(self):
        self.ensure_one()
        if not self._get_payment_due_checkout_sessions():
            raise UserError(
                "Patient statement is only available when unpaid checkout sessions exist."
            )
        return self.env.ref("hc_checkout.action_report_hc_patient_statement").report_action(
            self
        )
