from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class HcAppointment(models.Model):
    _name = "hc.appointment"
    _description = "Healthcare Appointment"
    _order = "start_datetime, id"
    _rec_name = "name"

    name = fields.Char(
        string="Appointment",
        compute="_compute_name",
        store=True,
    )

    patient_id = fields.Many2one(
        "res.partner",
        string="Patient",
        required=True,
        domain="[('is_hc_patient', '=', True)]",
        help="Patient scheduled for this appointment.",
    )
    practitioner_id = fields.Many2one(
        "hc.practitioner",
        string="Practitioner",
        required=True,
        help="Treating clinician assigned to this appointment.",
    )
    practice_id = fields.Many2one(
        "hc.practice",
        string="Practice",
        required=True,
        default=lambda self: self.env.user.practice_id,
        help="Practice handling this appointment.",
    )
    appointment_type_id = fields.Many2one(
        "hc.appointment.type",
        string="Appointment Type",
        required=True,
        help="Type of appointment being scheduled.",
    )
    start_datetime = fields.Datetime(
        string="Start",
        required=True,
        help="Appointment start date and time.",
    )
    end_datetime = fields.Datetime(
        string="End",
        required=True,
        help="Appointment end date and time.",
    )
    visit_status = fields.Selection(
        [
            ("scheduled", "Scheduled"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("closed", "Closed"),
        ],
        string="Visit Status",
        required=True,
        default="scheduled",
    )
    needs_follow_up = fields.Boolean(string="Needs Follow-Up")
    notes = fields.Text(help="Scheduling notes only.")

    @api.depends("patient_id", "appointment_type_id", "practitioner_id")
    def _compute_name(self):
        for record in self:
            parts = []
            if record.patient_id:
                parts.append(record.patient_id.display_name)
            if record.appointment_type_id:
                parts.append(record.appointment_type_id.display_name)
            elif record.practitioner_id:
                parts.append(record.practitioner_id.display_name)
            record.name = " - ".join(parts) or "Appointment"

    @api.constrains("start_datetime", "end_datetime")
    def _check_datetime_range(self):
        for record in self:
            if (
                record.start_datetime
                and record.end_datetime
                and record.end_datetime <= record.start_datetime
            ):
                raise ValidationError("Appointment end must be later than start.")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.name or "Appointment"))
        return result

    def action_start_visit(self):
        self.ensure_one()
        if self.intake_status != "complete" or self.consent_status != "complete":
            raise UserError(
                "Intake and consent must both be complete before starting the visit."
            )
        self.visit_status = "in_progress"
        return self.action_open_encounter()

    def action_complete_visit(self):
        self.ensure_one()
        encounter = self.env["hc.encounter"].search(
            [("appointment_id", "=", self.id)],
            limit=1,
        )
        if not encounter:
            raise UserError("An encounter is required before completing the visit.")
        encounter.write({"status": "complete"})
        self.visit_status = "completed"
        return True

    def action_close_visit(self):
        self.ensure_one()
        if self.visit_status != "completed":
            raise UserError("Only completed visits can be closed.")
        self.visit_status = "closed"
        return True

    def action_mark_needs_follow_up(self):
        self.ensure_one()
        if self.visit_status != "closed":
            raise UserError("Follow-up can only be managed after the visit is closed.")
        self.needs_follow_up = True
        return True

    def action_clear_follow_up(self):
        self.ensure_one()
        if self.visit_status != "closed":
            raise UserError("Follow-up can only be managed after the visit is closed.")
        self.needs_follow_up = False
        return True
