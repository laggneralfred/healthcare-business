import secrets

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class HcIntakeSubmission(models.Model):
    _name = "hc.intake.submission"
    _description = "Healthcare Intake Submission"
    _order = "submitted_on desc, id desc"
    _access_token_unique = models.Constraint(
        "unique(access_token)",
        "Each intake access token must be unique.",
    )

    @api.model
    def _find_default_template(self, practice_id=None):
        domain = [("active", "=", True)]
        if practice_id:
            domain.append(("practice_id", "=", practice_id))
        template = self.env["hc.intake.template"].search(domain, limit=1)
        if template:
            return template
        return self.env["hc.intake.template"].search([("active", "=", True)], limit=1)

    @api.model
    def _default_template_id(self):
        practice_id = self.env.context.get("default_practice_id") or self.env.user.practice_id.id
        return self._find_default_template(practice_id).id

    @api.model
    def _require_default_template(self, practice_id=None):
        template = self._find_default_template(practice_id)
        if not template:
            raise UserError(
                "Create an active Intake Template for this practice before recording intake."
            )
        return template

    @api.model
    def _find_latest_submission(self, patient_id=None, appointment_id=None):
        domain = []
        if appointment_id:
            domain.append(("appointment_id", "=", appointment_id))
        elif patient_id:
            domain.append(("patient_id", "=", patient_id))
        else:
            return self.env["hc.intake.submission"]
        return self.search(domain, order="submitted_on desc, id desc", limit=1)

    patient_id = fields.Many2one(
        "res.partner",
        string="Patient",
        required=True,
        domain="[('is_hc_patient', '=', True)]",
    )
    practice_id = fields.Many2one(
        "hc.practice",
        string="Practice",
        required=True,
        default=lambda self: self.env.user.practice_id,
    )
    appointment_id = fields.Many2one("hc.appointment", string="Appointment")
    template_id = fields.Many2one(
        "hc.intake.template",
        string="Intake Template",
        required=True,
        default=_default_template_id,
        domain="[('practice_id', '=', practice_id)]",
    )
    status = fields.Selection(
        [("missing", "Missing"), ("complete", "Complete")],
        string="Intake Status",
        required=True,
        default="complete",
    )
    submitted_on = fields.Datetime(string="Submitted On", default=fields.Datetime.now)
    access_token = fields.Char(copy=False, index=True)
    summary_text = fields.Text(string="Summary Notes")
    reason_for_visit = fields.Text(string="Reason for Visit")
    current_concerns = fields.Text(string="Current Concerns")
    relevant_history = fields.Text(string="Relevant History")
    medications = fields.Text(string="Medications")
    notes = fields.Text(string="Notes")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("template_id"):
                continue
            practice_id = vals.get("practice_id") or self.env.user.practice_id.id
            template = self._find_default_template(practice_id)
            if template:
                vals["template_id"] = template.id
        return super().create(vals_list)

    @api.model
    def _generate_access_token(self):
        token = secrets.token_urlsafe(32)
        while self.search_count([("access_token", "=", token)]):
            token = secrets.token_urlsafe(32)
        return token

    def _ensure_access_token(self):
        self.ensure_one()
        if not self.access_token:
            self.access_token = self._generate_access_token()
        return self.access_token

    def get_public_intake_url(self):
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url", "").rstrip("/")
        return "%s/intake/%s" % (base_url, self._ensure_access_token()) if base_url else "/intake/%s" % self._ensure_access_token()

    @api.model
    def _get_or_create_share_submission(self, patient_id=None, appointment_id=None, practice_id=None):
        submission = self._find_latest_submission(
            patient_id=patient_id,
            appointment_id=appointment_id,
        )
        if submission:
            submission._ensure_access_token()
            return submission

        if not patient_id or not practice_id:
            raise UserError("Patient and practice are required to share an intake link.")

        template = self._require_default_template(practice_id)
        submission = self.create(
            {
                "patient_id": patient_id,
                "practice_id": practice_id,
                "appointment_id": appointment_id or False,
                "template_id": template.id,
                "status": "missing",
                "submitted_on": False,
            }
        )
        submission._ensure_access_token()
        return submission

    def action_open_share_link_wizard(self):
        self.ensure_one()
        wizard = self.env["hc.intake.share.link.wizard"].create(
            {
                "intake_submission_id": self.id,
                "share_url": self.get_public_intake_url(),
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Patient Intake Link",
            "res_model": "hc.intake.share.link.wizard",
            "view_mode": "form",
            "res_id": wizard.id,
            "target": "new",
        }

    def _extract_public_submission_vals(self, values):
        self.ensure_one()
        return {
            "reason_for_visit": (values.get("reason_for_visit") or "").strip() or False,
            "current_concerns": (values.get("current_concerns") or "").strip() or False,
            "relevant_history": (values.get("relevant_history") or "").strip() or False,
            "medications": (values.get("medications") or "").strip() or False,
            "notes": (values.get("notes") or "").strip() or False,
        }

    def action_submit_public_intake(self, values):
        self.ensure_one()
        intake_vals = self._extract_public_submission_vals(values)
        if not any(intake_vals.values()):
            raise ValidationError(
                "Complete intake records must include at least one intake content field."
            )
        intake_vals.update(
            {
                "status": "complete",
                "submitted_on": fields.Datetime.now(),
            }
        )
        self.write(intake_vals)

    @api.constrains(
        "status",
        "reason_for_visit",
        "current_concerns",
        "relevant_history",
        "medications",
        "notes",
    )
    def _check_complete_intake_has_content(self):
        for record in self:
            if record.status != "complete":
                continue
            has_content = any(
                (
                    (record.reason_for_visit or "").strip(),
                    (record.current_concerns or "").strip(),
                    (record.relevant_history or "").strip(),
                    (record.medications or "").strip(),
                    (record.notes or "").strip(),
                )
            )
            if not has_content:
                raise ValidationError(
                    "Complete intake records must include at least one intake content field."
                )
