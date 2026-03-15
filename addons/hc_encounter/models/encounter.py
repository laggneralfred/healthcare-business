from odoo import api, fields, models


class HcEncounter(models.Model):
    _name = "hc.encounter"
    _description = "Healthcare Encounter"
    _order = "encounter_date desc, id desc"
    _rec_name = "name"
    _appointment_unique = models.Constraint(
        "unique(appointment_id)",
        "Each appointment can only have one encounter.",
    )

    name = fields.Char(
        string="Encounter",
        compute="_compute_name",
        store=True,
    )
    patient_id = fields.Many2one(
        "res.partner",
        string="Patient",
        required=True,
        domain="[('is_hc_patient', '=', True)]",
    )
    appointment_id = fields.Many2one(
        "hc.appointment",
        string="Appointment",
        required=True,
    )
    practice_id = fields.Many2one(
        "hc.practice",
        string="Practice",
        required=True,
    )
    practitioner_id = fields.Many2one(
        "hc.practitioner",
        string="Practitioner",
        required=True,
    )
    intake_status = fields.Selection(
        [("missing", "Missing"), ("complete", "Complete")],
        string="Intake Status",
        compute="_compute_readiness_statuses",
    )
    consent_status = fields.Selection(
        [("missing", "Missing"), ("complete", "Complete")],
        string="Consent Status",
        compute="_compute_readiness_statuses",
    )
    status = fields.Selection(
        [("draft", "Draft"), ("complete", "Complete")],
        string="Status",
        required=True,
        default="draft",
    )
    encounter_date = fields.Datetime(
        string="Encounter Date",
        required=True,
        default=fields.Datetime.now,
    )
    completed_on = fields.Datetime(string="Completed On")
    chief_concern = fields.Text(string="Chief Concern")
    visit_summary = fields.Text(string="Visit Summary")
    treatment_notes = fields.Text(string="Treatment Notes")
    notes = fields.Text(string="Notes")

    @api.depends("patient_id", "encounter_date")
    def _compute_name(self):
        for record in self:
            patient_name = record.patient_id.display_name or "Encounter"
            if record.encounter_date:
                record.name = "%s - %s" % (
                    patient_name,
                    fields.Datetime.to_string(record.encounter_date),
                )
            else:
                record.name = patient_name

    @api.depends("appointment_id", "patient_id")
    def _compute_readiness_statuses(self):
        Submission = self.env["hc.intake.submission"]
        ConsentRecord = self.env["hc.consent.record"]
        for record in self:
            latest_intake = self.env["hc.intake.submission"]
            latest_consent = self.env["hc.consent.record"]

            if record.appointment_id:
                latest_intake = Submission.search(
                    [("appointment_id", "=", record.appointment_id.id)],
                    order="submitted_on desc, id desc",
                    limit=1,
                )
                latest_consent = ConsentRecord.search(
                    [("appointment_id", "=", record.appointment_id.id)],
                    order="signed_on desc, id desc",
                    limit=1,
                )

            if not latest_intake and record.patient_id:
                latest_intake = Submission.search(
                    [
                        ("patient_id", "=", record.patient_id.id),
                        ("appointment_id", "=", False),
                    ],
                    order="submitted_on desc, id desc",
                    limit=1,
                )

            if not latest_consent and record.patient_id:
                latest_consent = ConsentRecord.search(
                    [
                        ("patient_id", "=", record.patient_id.id),
                        ("appointment_id", "=", False),
                    ],
                    order="signed_on desc, id desc",
                    limit=1,
                )

            record.intake_status = latest_intake.status or "missing"
            record.consent_status = latest_consent.status or "missing"

    def action_open_intake(self):
        self.ensure_one()
        return self.appointment_id.action_record_intake()

    def action_open_consent(self):
        self.ensure_one()
        return self.appointment_id.action_record_consent()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("status") == "complete" and "completed_on" not in vals:
                vals["completed_on"] = fields.Datetime.now()
            elif vals.get("status") == "draft" and "completed_on" not in vals:
                vals["completed_on"] = False
        return super().create(vals_list)

    def write(self, vals):
        if "status" in vals and "completed_on" not in vals:
            vals = dict(vals)
            vals["completed_on"] = (
                fields.Datetime.now() if vals["status"] == "complete" else False
            )
        return super().write(vals)
