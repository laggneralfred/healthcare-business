from odoo import fields, models


class HcAppointment(models.Model):
    _inherit = "hc.appointment"

    def action_open_encounter(self):
        self.ensure_one()
        encounter = self.env["hc.encounter"].search(
            [("appointment_id", "=", self.id)],
            limit=1,
        )
        if not encounter:
            encounter = self.env["hc.encounter"].create(
                {
                    "patient_id": self.patient_id.id,
                    "appointment_id": self.id,
                    "practice_id": self.practice_id.id,
                    "practitioner_id": self.practitioner_id.id,
                    "encounter_date": self.start_datetime or fields.Datetime.now(),
                }
            )
        view = self.env.ref("hc_encounter.view_hc_encounter_form")
        return {
            "type": "ir.actions.act_window",
            "name": "Encounter",
            "res_model": "hc.encounter",
            "view_mode": "form",
            "view_id": view.id,
            "res_id": encounter.id,
            "target": "new",
        }
