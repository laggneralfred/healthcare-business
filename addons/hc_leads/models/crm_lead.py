from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"
    _description = "Healthcare Lead"
    _rec_name = "name"

    is_hc_lead = fields.Boolean(
        string="Healthcare Lead",
        default=True,
        help="Marks this CRM lead as part of the Sprint 1 healthcare workflow.",
    )
    practice_id = fields.Many2one(
        "hc.practice",
        string="Practice",
        help="Practice associated with this lead.",
    )

    def action_create_patient(self):
        self.ensure_one()

        patient = self.env["res.partner"].create(
            {
                "name": self.name,
                "phone": self.phone,
                "email": self.email_from,
                "practice_id": self.practice_id.id,
                "comment": self.description,
                "is_hc_patient": True,
            }
        )
        return self._action_open_patient(patient)

    def _action_open_patient(self, patient):
        return {
            "type": "ir.actions.act_window",
            "name": "Patient",
            "res_model": "res.partner",
            "res_id": patient.id,
            "view_mode": "form",
            "target": "current",
        }
