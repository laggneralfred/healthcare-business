from odoo import api, fields, models
from odoo.exceptions import UserError


class HcAppointment(models.Model):
    _inherit = "hc.appointment"

    checkout_session_ids = fields.One2many(
        "hc.checkout.session",
        "appointment_id",
        string="Checkout Sessions",
    )
    checkout_session_id = fields.Many2one(
        "hc.checkout.session",
        string="Checkout Session",
        compute="_compute_checkout_summary",
        compute_sudo=True,
    )
    checkout_status = fields.Selection(
        [
            ("none", "None"),
            ("open", "Open"),
            ("paid", "Paid"),
            ("payment_due", "Payment Due"),
        ],
        string="Checkout Status",
        compute="_compute_checkout_summary",
        compute_sudo=True,
    )
    checkout_amount_total = fields.Monetary(
        string="Checkout Amount",
        compute="_compute_checkout_summary",
        compute_sudo=True,
        currency_field="checkout_currency_id",
    )
    checkout_paid_on = fields.Datetime(
        string="Checkout Paid On",
        compute="_compute_checkout_summary",
        compute_sudo=True,
    )
    checkout_tender_type = fields.Selection(
        [
            ("cash", "Cash"),
            ("card", "Card"),
        ],
        string="Checkout Tender",
        compute="_compute_checkout_summary",
        compute_sudo=True,
    )
    checkout_currency_id = fields.Many2one(
        "res.currency",
        string="Checkout Currency",
        compute="_compute_checkout_summary",
        compute_sudo=True,
    )

    @api.depends(
        "checkout_session_ids",
        "checkout_session_ids.state",
        "checkout_session_ids.amount_total",
        "checkout_session_ids.tender_type",
        "checkout_session_ids.paid_on",
        "checkout_session_ids.currency_id",
    )
    def _compute_checkout_summary(self):
        company_currency = self.env.company.currency_id
        for appointment in self:
            session = appointment.checkout_session_ids[:1]
            appointment.checkout_session_id = session
            appointment.checkout_status = session.state or "none"
            appointment.checkout_amount_total = session.amount_total if session else 0.0
            appointment.checkout_paid_on = session.paid_on if session else False
            appointment.checkout_tender_type = session.tender_type if session else False
            appointment.checkout_currency_id = session.currency_id or company_currency

    def action_start_checkout(self):
        self.ensure_one()
        if self.visit_status != "closed":
            raise UserError("Checkout can only be started after the visit is closed.")
        session = self.env["hc.checkout.session"].search(
            [("appointment_id", "=", self.id)],
            limit=1,
        )
        if not session:
            session = self.env["hc.checkout.session"].create(
                {
                    "appointment_id": self.id,
                }
            )
        view = self.env.ref("hc_checkout.view_hc_checkout_session_form")
        return {
            "type": "ir.actions.act_window",
            "name": "Checkout",
            "res_model": "hc.checkout.session",
            "view_mode": "form",
            "view_id": view.id,
            "res_id": session.id,
        }
