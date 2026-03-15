import secrets

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class HcConsentRecord(models.Model):
    _name = "hc.consent.record"
    _description = "Healthcare Consent Record"
    _order = "signed_on desc, id desc"
    _access_token_unique = models.Constraint(
        "unique(access_token)",
        "Each consent access token must be unique.",
    )

    @api.model
    def _find_default_template(self, practice_id=None):
        domain = [("active", "=", True)]
        if practice_id:
            domain.append(("practice_id", "=", practice_id))
        template = self.env["hc.consent.template"].search(domain, limit=1)
        if template:
            return template
        return self.env["hc.consent.template"].search([("active", "=", True)], limit=1)

    @api.model
    def _default_template_id(self):
        practice_id = self.env.context.get("default_practice_id") or self.env.user.practice_id.id
        return self._find_default_template(practice_id).id

    @api.model
    def _require_default_template(self, practice_id=None):
        template = self._find_default_template(practice_id)
        if not template:
            raise UserError(
                "Create an active Consent Template for this practice before recording consent."
            )
        return template

    @api.model
    def _find_latest_record(self, patient_id=None, appointment_id=None):
        domain = []
        if appointment_id:
            domain.append(("appointment_id", "=", appointment_id))
        elif patient_id:
            domain.append(("patient_id", "=", patient_id))
        else:
            return self.env["hc.consent.record"]
        return self.search(domain, order="signed_on desc, id desc", limit=1)

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
        "hc.consent.template",
        string="Consent Template",
        required=True,
        default=_default_template_id,
        domain="[('practice_id', '=', practice_id)]",
    )
    status = fields.Selection(
        [("missing", "Missing"), ("complete", "Complete")],
        string="Consent Status",
        required=True,
        default="complete",
    )
    signed_on = fields.Datetime(string="Signed On", default=fields.Datetime.now)
    access_token = fields.Char(copy=False, index=True)
    consent_given_by = fields.Char(string="Consent Given By")
    consent_summary = fields.Text(string="Consent Summary")
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

    def get_public_consent_url(self):
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url", "").rstrip("/")
        return "%s/consent/%s" % (base_url, self._ensure_access_token()) if base_url else "/consent/%s" % self._ensure_access_token()

    @api.model
    def _get_or_create_share_record(self, patient_id=None, appointment_id=None, practice_id=None):
        record = self._find_latest_record(
            patient_id=patient_id,
            appointment_id=appointment_id,
        )
        if record:
            record._ensure_access_token()
            return record

        if not patient_id or not practice_id:
            raise UserError("Patient and practice are required to share a consent link.")

        template = self._require_default_template(practice_id)
        record = self.create(
            {
                "patient_id": patient_id,
                "practice_id": practice_id,
                "appointment_id": appointment_id or False,
                "template_id": template.id,
                "status": "missing",
                "signed_on": False,
            }
        )
        record._ensure_access_token()
        return record

    def action_open_share_link_wizard(self):
        self.ensure_one()
        wizard = self.env["hc.consent.share.link.wizard"].create(
            {
                "consent_record_id": self.id,
                "share_url": self.get_public_consent_url(),
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Patient Consent Link",
            "res_model": "hc.consent.share.link.wizard",
            "view_mode": "form",
            "res_id": wizard.id,
            "target": "new",
        }

    def _extract_public_consent_vals(self, values):
        self.ensure_one()
        return {
            "consent_given_by": (values.get("consent_given_by") or "").strip() or False,
            "consent_summary": (values.get("consent_summary") or "").strip() or False,
            "notes": (values.get("notes") or "").strip() or False,
        }

    def action_submit_public_consent(self, values):
        self.ensure_one()
        consent_vals = self._extract_public_consent_vals(values)
        if not any(consent_vals.values()):
            raise ValidationError(
                "Complete consent records must include at least one consent content field."
            )
        consent_vals.update(
            {
                "status": "complete",
                "signed_on": fields.Datetime.now(),
            }
        )
        self.write(consent_vals)

    @api.constrains("status", "consent_given_by", "consent_summary", "notes")
    def _check_complete_consent_has_content(self):
        for record in self:
            if record.status != "complete":
                continue
            has_content = any(
                (
                    (record.consent_given_by or "").strip(),
                    (record.consent_summary or "").strip(),
                    (record.notes or "").strip(),
                )
            )
            if not has_content:
                raise ValidationError(
                    "Complete consent records must include at least one consent content field."
                )
