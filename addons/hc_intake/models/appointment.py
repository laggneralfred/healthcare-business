from odoo import api, fields, models


class HcAppointment(models.Model):
    _inherit = "hc.appointment"

    intake_status = fields.Selection(
        [("missing", "Missing"), ("complete", "Complete")],
        string="Intake Status",
        compute="_compute_intake_status",
    )

    @api.depends("patient_id")
    def _compute_intake_status(self):
        Submission = self.env["hc.intake.submission"]
        for record in self:
            latest = Submission.search(
                [("appointment_id", "=", record.id)],
                order="submitted_on desc, id desc",
                limit=1,
            )
            if not latest and record.patient_id:
                latest = Submission.search(
                    [
                        ("patient_id", "=", record.patient_id.id),
                        ("appointment_id", "=", False),
                    ],
                    order="submitted_on desc, id desc",
                    limit=1,
                )
            record.intake_status = latest.status or "missing"

    def action_record_intake(self):
        self.ensure_one()
        view = self.env.ref("hc_intake.view_hc_intake_submission_form")
        Submission = self.env["hc.intake.submission"]
        existing = Submission._find_latest_submission(appointment_id=self.id)
        action = {
            "type": "ir.actions.act_window",
            "name": "Record Intake",
            "res_model": "hc.intake.submission",
            "view_mode": "form",
            "view_id": view.id,
            "target": "new",
        }
        if existing:
            action["res_id"] = existing.id
        else:
            template_id = Submission._require_default_template(self.practice_id.id).id
            action["context"] = {
                "default_patient_id": self.patient_id.id,
                "default_practice_id": self.practice_id.id,
                "default_appointment_id": self.id,
                "default_template_id": template_id,
                "default_status": "complete",
                "default_submitted_on": fields.Datetime.now(),
            }
        return action

    def action_share_intake_link(self):
        self.ensure_one()
        submission = self.env["hc.intake.submission"]._get_or_create_share_submission(
            patient_id=self.patient_id.id,
            appointment_id=self.id,
            practice_id=self.practice_id.id,
        )
        return submission.action_open_share_link_wizard()
