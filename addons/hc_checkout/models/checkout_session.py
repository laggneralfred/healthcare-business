from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class HcCheckoutSession(models.Model):
    _name = "hc.checkout.session"
    _description = "Healthcare Checkout Session"
    _order = "started_on desc, id desc"

    name = fields.Char(
        string="Checkout",
        required=True,
        default="New",
        copy=False,
    )
    appointment_id = fields.Many2one(
        "hc.appointment",
        string="Appointment",
        required=True,
        ondelete="cascade",
    )
    patient_id = fields.Many2one(
        "res.partner",
        string="Patient",
        required=True,
        readonly=True,
    )
    practitioner_id = fields.Many2one(
        "hc.practitioner",
        string="Practitioner",
        readonly=True,
    )
    appointment_start = fields.Datetime(
        string="Appointment Start",
        readonly=True,
    )
    state = fields.Selection(
        [
            ("open", "Open"),
            ("paid", "Paid"),
            ("payment_due", "Payment Due"),
        ],
        string="State",
        required=True,
        default="open",
    )
    charge_label = fields.Char(
        string="Charge Label",
        required=True,
    )
    amount_total = fields.Monetary(
        string="Amount Total",
        required=True,
        default=0.0,
        currency_field="currency_id",
    )
    amount_paid = fields.Monetary(
        string="Amount Paid",
        default=0.0,
        currency_field="currency_id",
        readonly=True,
    )
    tender_type = fields.Selection(
        [
            ("cash", "Cash"),
            ("card", "Card"),
        ],
        string="Tender",
        readonly=True,
    )
    started_on = fields.Datetime(
        string="Started On",
        required=True,
        default=fields.Datetime.now,
        readonly=True,
    )
    paid_on = fields.Datetime(
        string="Paid On",
        readonly=True,
    )
    payment_note = fields.Char(string="Payment Note")
    notes = fields.Text(string="Internal Notes")
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    checkout_line_ids = fields.One2many(
        "hc.checkout.line",
        "checkout_session_id",
        string="Checkout Lines",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            appointment = None
            appointment_id = vals.get("appointment_id")
            if appointment_id:
                appointment = self.env["hc.appointment"].browse(appointment_id)
                if appointment.exists():
                    vals.setdefault("patient_id", appointment.patient_id.id)
                    vals.setdefault("practitioner_id", appointment.practitioner_id.id)
                    vals.setdefault("appointment_start", appointment.start_datetime)
                    vals.setdefault(
                        "charge_label",
                        appointment.appointment_type_id.display_name
                        or appointment.name
                        or "Visit Charge",
                    )
                    vals.setdefault(
                        "name",
                        f"CHK/{appointment.id}",
                    )
            if not vals.get("name") and not appointment:
                vals["name"] = "Checkout"
        records = super().create(vals_list)
        if not self.env.context.get("skip_default_line_creation"):
            records._create_default_line_if_missing()
        return records

    def _register_hook(self):
        result = super()._register_hook()
        self.sudo()._backfill_missing_checkout_lines()
        return result

    def _prepare_default_line_vals(self):
        self.ensure_one()
        vals = {
            "checkout_session_id": self.id,
            "sequence": 10,
            "description": self.charge_label or "Visit Charge",
            "amount": self.amount_total,
        }
        line_model = self.env["hc.checkout.line"]
        if (
            "service_fee_id" in line_model._fields
            and "service_fee_id" in self._fields
            and getattr(self, "service_fee_id", False)
        ):
            vals["service_fee_id"] = self.service_fee_id.id
        return vals

    def _create_default_line_if_missing(self):
        line_env = self.env["hc.checkout.line"].with_context(
            allow_locked_checkout_line_write=True
        )
        for record in self:
            if record.checkout_line_ids:
                continue
            line_env.create(record._prepare_default_line_vals())

    def _backfill_missing_checkout_lines(self):
        sessions = self.search([]).filtered(lambda record: not record.checkout_line_ids)
        if sessions:
            sessions._create_default_line_if_missing()

    def _sync_from_lines(self):
        for record in self:
            lines = record.checkout_line_ids.sorted(key=lambda line: (line.sequence, line.id))
            total = sum(lines.mapped("amount"))
            vals = {
                "amount_total": total,
            }
            if lines:
                vals["charge_label"] = lines[0].description
                if "service_fee_id" in record._fields and "service_fee_id" in lines[0]._fields:
                    vals["service_fee_id"] = lines[0].service_fee_id.id or False
            record.with_context(skip_session_service_fee_apply=True).write(vals)

    def _check_closed_appointment(self):
        for record in self:
            if record.appointment_id.visit_status != "closed":
                raise ValidationError("Checkout can only be created for closed appointments.")

    def _check_unique_appointment(self):
        for record in self:
            if not record.appointment_id:
                continue
            duplicate_count = self.search_count(
                [
                    ("appointment_id", "=", record.appointment_id.id),
                    ("id", "!=", record.id),
                ]
            )
            if duplicate_count:
                raise ValidationError("Only one checkout session is allowed per appointment.")

    def _check_nonnegative_amounts(self):
        for record in self:
            if record.amount_total < 0:
                raise ValidationError("Checkout amount total must be zero or greater.")
            if record.amount_paid < 0:
                raise ValidationError("Checkout amount paid must be zero or greater.")

    def _check_paid_state_values(self):
        for record in self:
            if record.state == "paid":
                if record.tender_type not in {"cash", "card"}:
                    raise ValidationError("Paid checkout sessions must include cash or card.")
                if record.amount_paid != record.amount_total:
                    raise ValidationError(
                        "Paid checkout sessions must record the full amount as paid."
                    )
                if not record.paid_on:
                    raise ValidationError("Paid checkout sessions must include a paid date.")
            if record.state == "payment_due":
                if record.tender_type:
                    raise ValidationError(
                        "Payment due checkout sessions cannot include a tender type."
                    )
                if record.amount_paid:
                    raise ValidationError(
                        "Payment due checkout sessions cannot include an amount paid."
                    )
                if record.paid_on:
                    raise ValidationError(
                        "Payment due checkout sessions cannot include a paid date."
                    )

    @api.constrains("appointment_id")
    def _constrain_appointment_id(self):
        self._check_closed_appointment()
        self._check_unique_appointment()

    @api.constrains("state", "amount_total", "amount_paid", "tender_type", "paid_on")
    def _constrain_state_values(self):
        self._check_nonnegative_amounts()
        self._check_paid_state_values()

    def _ensure_open_state(self):
        self.ensure_one()
        if self.state != "open":
            raise UserError("Only open checkout sessions can be updated.")

    def action_mark_cash_paid(self):
        self.ensure_one()
        self._ensure_open_state()
        self.write(
            {
                "state": "paid",
                "tender_type": "cash",
                "amount_paid": self.amount_total,
                "paid_on": fields.Datetime.now(),
            }
        )
        return True

    def action_mark_card_paid(self):
        self.ensure_one()
        self._ensure_open_state()
        self.write(
            {
                "state": "paid",
                "tender_type": "card",
                "amount_paid": self.amount_total,
                "paid_on": fields.Datetime.now(),
            }
        )
        return True

    def action_mark_payment_due(self):
        self.ensure_one()
        self._ensure_open_state()
        self.write(
            {
                "state": "payment_due",
                "tender_type": False,
                "amount_paid": 0.0,
                "paid_on": False,
            }
        )
        return True
