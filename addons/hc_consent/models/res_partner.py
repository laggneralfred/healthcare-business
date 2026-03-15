from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    consent_status = fields.Selection(
        [("missing", "Missing"), ("complete", "Complete")],
        string="Consent Status",
        compute="_compute_consent_status",
    )

    @api.depends("is_hc_patient")
    def _compute_consent_status(self):
        Record = self.env["hc.consent.record"]
        for record in self:
            latest = Record.search(
                [("patient_id", "=", record.id)],
                order="signed_on desc, id desc",
                limit=1,
            )
            record.consent_status = latest.status or "missing"

    def action_record_consent(self):
        self.ensure_one()
        view = self.env.ref("hc_consent.view_hc_consent_record_form")
        Record = self.env["hc.consent.record"]
        existing = Record._find_latest_record(patient_id=self.id)
        action = {
            "type": "ir.actions.act_window",
            "name": "Record Consent",
            "res_model": "hc.consent.record",
            "view_mode": "form",
            "view_id": view.id,
            "target": "new",
        }
        if existing:
            action["res_id"] = existing.id
        else:
            template_id = Record._require_default_template(self.practice_id.id).id
            action["context"] = {
                "default_patient_id": self.id,
                "default_practice_id": self.practice_id.id,
                "default_template_id": template_id,
                "default_status": "complete",
                "default_signed_on": fields.Datetime.now(),
            }
        return action

    def action_share_consent_link(self):
        self.ensure_one()
        record = self.env["hc.consent.record"]._get_or_create_share_record(
            patient_id=self.id,
            practice_id=self.practice_id.id,
        )
        return record.action_open_share_link_wizard()
