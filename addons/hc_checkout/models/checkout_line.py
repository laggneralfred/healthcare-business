from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class HcCheckoutLine(models.Model):
    _name = "hc.checkout.line"
    _description = "Healthcare Checkout Line"
    _order = "sequence, id"

    checkout_session_id = fields.Many2one(
        "hc.checkout.session",
        string="Checkout Session",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(default=10)
    description = fields.Char(required=True)
    amount = fields.Monetary(
        required=True,
        default=0.0,
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="checkout_session_id.currency_id",
        readonly=True,
        store=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        sessions = self.env["hc.checkout.session"]
        for vals in vals_list:
            session = self.env["hc.checkout.session"].browse(vals["checkout_session_id"])
            sessions |= session
            if (
                session.state != "open"
                and not self.env.context.get("allow_locked_checkout_line_write")
            ):
                raise UserError("Checkout lines can only be changed while checkout is open.")
        records = super().create(vals_list)
        sessions._sync_from_lines()
        return records

    def write(self, vals):
        sessions = self.mapped("checkout_session_id")
        if (
            any(session.state != "open" for session in sessions)
            and not self.env.context.get("allow_locked_checkout_line_write")
        ):
            raise UserError("Checkout lines can only be changed while checkout is open.")
        result = super().write(vals)
        sessions._sync_from_lines()
        return result

    def unlink(self):
        sessions = self.mapped("checkout_session_id")
        if (
            any(session.state != "open" for session in sessions)
            and not self.env.context.get("allow_locked_checkout_line_write")
        ):
            raise UserError("Checkout lines can only be changed while checkout is open.")
        result = super().unlink()
        sessions._sync_from_lines()
        return result

    @api.constrains("amount")
    def _check_amount(self):
        for record in self:
            if record.amount < 0:
                raise ValidationError("Checkout line amount must be zero or greater.")
