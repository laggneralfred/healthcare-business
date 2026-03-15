from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_hc_patient = fields.Boolean(string="Healthcare Patient", default=False)
    practice_id = fields.Many2one(
        "hc.practice",
        string="Practice",
        help="Primary practice for this patient.",
    )

    def action_create_appointment(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Create Appointment",
            "res_model": "hc.appointment",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_patient_id": self.id,
                "default_practice_id": self.practice_id.id,
            },
        }
