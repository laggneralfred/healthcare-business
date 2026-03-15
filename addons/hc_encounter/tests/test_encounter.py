from datetime import timedelta

from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestEncounter(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.practice = cls.env["hc.practice"].create(
            {
                "name": "Encounter Test Practice",
            }
        )
        cls.patient = cls.env["res.partner"].create(
            {
                "name": "Encounter Test Patient",
                "is_hc_patient": True,
                "practice_id": cls.practice.id,
            }
        )
        cls.practitioner = cls.env["hc.practitioner"].create(
            {
                "name": "Encounter Test Practitioner",
                "practice_id": cls.practice.id,
            }
        )
        cls.appointment_type = cls.env["hc.appointment.type"].create(
            {
                "name": "Encounter Test Visit",
                "practice_id": cls.practice.id,
            }
        )
        cls.intake_template = cls.env["hc.intake.template"].create(
            {
                "name": "Encounter Test Intake Template",
                "practice_id": cls.practice.id,
                "active": True,
            }
        )
        cls.consent_template = cls.env["hc.consent.template"].create(
            {
                "name": "Encounter Test Consent Template",
                "practice_id": cls.practice.id,
                "active": True,
            }
        )

    def _create_appointment(self):
        start_datetime = fields.Datetime.now()
        return self.env["hc.appointment"].create(
            {
                "patient_id": self.patient.id,
                "practitioner_id": self.practitioner.id,
                "practice_id": self.practice.id,
                "appointment_type_id": self.appointment_type.id,
                "start_datetime": start_datetime,
                "end_datetime": start_datetime + timedelta(hours=1),
            }
        )

    def _action_res_id(self, action):
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "hc.encounter")
        return action["res_id"]

    def _create_encounter(self, appointment):
        return self.env["hc.encounter"].create(
            {
                "patient_id": appointment.patient_id.id,
                "appointment_id": appointment.id,
                "practice_id": appointment.practice_id.id,
                "practitioner_id": appointment.practitioner_id.id,
                "encounter_date": appointment.start_datetime,
            }
        )

    def test_open_encounter_creates_one_if_missing(self):
        appointment = self._create_appointment()

        action = appointment.action_open_encounter()
        encounter = self.env["hc.encounter"].browse(self._action_res_id(action))

        self.assertTrue(encounter.exists())
        self.assertEqual(encounter.patient_id, appointment.patient_id)
        self.assertEqual(encounter.appointment_id, appointment)
        self.assertEqual(encounter.practice_id, appointment.practice_id)
        self.assertEqual(encounter.practitioner_id, appointment.practitioner_id)
        self.assertEqual(encounter.status, "draft")
        self.assertEqual(encounter.encounter_date, appointment.start_datetime)

    def test_open_encounter_reopens_existing_record(self):
        appointment = self._create_appointment()

        first_action = appointment.action_open_encounter()
        second_action = appointment.action_open_encounter()

        first_encounter = self.env["hc.encounter"].browse(self._action_res_id(first_action))
        second_encounter = self.env["hc.encounter"].browse(self._action_res_id(second_action))

        self.assertEqual(first_encounter, second_encounter)
        self.assertEqual(
            self.env["hc.encounter"].search_count([("appointment_id", "=", appointment.id)]),
            1,
        )

    def test_encounter_can_store_notes_and_status(self):
        appointment = self._create_appointment()
        action = appointment.action_open_encounter()
        encounter = self.env["hc.encounter"].browse(self._action_res_id(action))

        encounter.write(
            {
                "notes": "Minimal encounter notes",
                "status": "complete",
            }
        )

        encounter.invalidate_recordset(["notes", "status"])
        self.assertEqual(encounter.notes, "Minimal encounter notes")
        self.assertEqual(encounter.status, "complete")

    def test_encounter_can_store_visit_summary(self):
        appointment = self._create_appointment()
        encounter = self._create_encounter(appointment)

        encounter.write(
            {
                "visit_summary": "Short provider-facing summary",
                "notes": "Longer supporting note",
            }
        )

        encounter.invalidate_recordset(["visit_summary", "notes"])
        self.assertEqual(encounter.visit_summary, "Short provider-facing summary")
        self.assertEqual(encounter.notes, "Longer supporting note")

    def test_encounter_can_store_chief_concern(self):
        appointment = self._create_appointment()
        encounter = self._create_encounter(appointment)

        encounter.write(
            {
                "chief_concern": "Persistent shoulder pain",
                "visit_summary": "Provider reviewed the main complaint",
                "notes": "Patient reports symptoms worsening this week",
            }
        )

        encounter.invalidate_recordset(["chief_concern", "visit_summary", "notes"])
        self.assertEqual(encounter.chief_concern, "Persistent shoulder pain")
        self.assertEqual(encounter.visit_summary, "Provider reviewed the main complaint")
        self.assertEqual(encounter.notes, "Patient reports symptoms worsening this week")

    def test_encounter_can_store_treatment_notes(self):
        appointment = self._create_appointment()
        encounter = self._create_encounter(appointment)

        encounter.write(
            {
                "chief_concern": "Lower back pain",
                "visit_summary": "Evaluated symptoms and discussed next steps",
                "treatment_notes": "Performed exam and provided home care guidance",
                "notes": "Patient tolerated the visit well",
            }
        )

        encounter.invalidate_recordset(
            ["chief_concern", "visit_summary", "treatment_notes", "notes"]
        )
        self.assertEqual(encounter.chief_concern, "Lower back pain")
        self.assertEqual(encounter.visit_summary, "Evaluated symptoms and discussed next steps")
        self.assertEqual(
            encounter.treatment_notes,
            "Performed exam and provided home care guidance",
        )
        self.assertEqual(encounter.notes, "Patient tolerated the visit well")

    def test_completed_on_follows_status(self):
        appointment = self._create_appointment()
        encounter = self._create_encounter(appointment)

        self.assertFalse(encounter.completed_on)

        encounter.write({"status": "complete"})
        encounter.invalidate_recordset(["status", "completed_on"])
        self.assertEqual(encounter.status, "complete")
        self.assertTrue(encounter.completed_on)

        encounter.write({"status": "draft"})
        encounter.invalidate_recordset(["status", "completed_on"])
        self.assertEqual(encounter.status, "draft")
        self.assertFalse(encounter.completed_on)

    def test_open_intake_delegates_to_existing_appointment_logic(self):
        appointment = self._create_appointment()
        encounter = self._create_encounter(appointment)

        appointment_action_missing = appointment.action_record_intake()
        encounter_action_missing = encounter.action_open_intake()

        self.assertEqual(appointment_action_missing, encounter_action_missing)
        self.assertEqual(encounter_action_missing["res_model"], "hc.intake.submission")
        self.assertFalse(encounter_action_missing.get("res_id"))

        submission = self.env["hc.intake.submission"].create(
            {
                "patient_id": self.patient.id,
                "practice_id": self.practice.id,
                "appointment_id": appointment.id,
                "template_id": self.intake_template.id,
                "status": "complete",
                "reason_for_visit": "Encounter shortcut intake test",
                "submitted_on": fields.Datetime.now(),
            }
        )

        appointment_action_existing = appointment.action_record_intake()
        encounter_action_existing = encounter.action_open_intake()

        self.assertEqual(appointment_action_existing, encounter_action_existing)
        self.assertEqual(encounter_action_existing["res_model"], "hc.intake.submission")
        self.assertEqual(encounter_action_existing["res_id"], submission.id)

    def test_open_consent_delegates_to_existing_appointment_logic(self):
        appointment = self._create_appointment()
        encounter = self._create_encounter(appointment)

        appointment_action_missing = appointment.action_record_consent()
        encounter_action_missing = encounter.action_open_consent()

        self.assertEqual(appointment_action_missing, encounter_action_missing)
        self.assertEqual(encounter_action_missing["res_model"], "hc.consent.record")
        self.assertFalse(encounter_action_missing.get("res_id"))

        record = self.env["hc.consent.record"].create(
            {
                "patient_id": self.patient.id,
                "practice_id": self.practice.id,
                "appointment_id": appointment.id,
                "template_id": self.consent_template.id,
                "status": "complete",
                "consent_summary": "Encounter shortcut consent test",
                "signed_on": fields.Datetime.now(),
            }
        )

        appointment_action_existing = appointment.action_record_consent()
        encounter_action_existing = encounter.action_open_consent()

        self.assertEqual(appointment_action_existing, encounter_action_existing)
        self.assertEqual(encounter_action_existing["res_model"], "hc.consent.record")
        self.assertEqual(encounter_action_existing["res_id"], record.id)
