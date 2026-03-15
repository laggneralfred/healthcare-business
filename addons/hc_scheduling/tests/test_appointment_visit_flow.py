from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestAppointmentVisitFlow(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.practice = cls.env["hc.practice"].create(
            {
                "name": "Visit Flow Test Practice",
            }
        )
        cls.patient = cls.env["res.partner"].create(
            {
                "name": "Visit Flow Test Patient",
                "is_hc_patient": True,
                "practice_id": cls.practice.id,
            }
        )
        cls.practitioner = cls.env["hc.practitioner"].create(
            {
                "name": "Visit Flow Test Practitioner",
                "practice_id": cls.practice.id,
            }
        )
        cls.appointment_type = cls.env["hc.appointment.type"].create(
            {
                "name": "Visit Flow Test Appointment Type",
                "practice_id": cls.practice.id,
            }
        )
        cls.intake_template = cls.env["hc.intake.template"].create(
            {
                "name": "Visit Flow Test Intake Template",
                "practice_id": cls.practice.id,
                "active": True,
            }
        )
        cls.consent_template = cls.env["hc.consent.template"].create(
            {
                "name": "Visit Flow Test Consent Template",
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

    def _create_complete_readiness(self, appointment):
        self.env["hc.intake.submission"].create(
            {
                "patient_id": appointment.patient_id.id,
                "practice_id": appointment.practice_id.id,
                "appointment_id": appointment.id,
                "template_id": self.intake_template.id,
                "status": "complete",
                "reason_for_visit": "Visit flow readiness test",
                "submitted_on": fields.Datetime.now(),
            }
        )
        self.env["hc.consent.record"].create(
            {
                "patient_id": appointment.patient_id.id,
                "practice_id": appointment.practice_id.id,
                "appointment_id": appointment.id,
                "template_id": self.consent_template.id,
                "status": "complete",
                "consent_summary": "Visit flow readiness test",
                "signed_on": fields.Datetime.now(),
            }
        )

    def _assert_encounter_action(self, action):
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "hc.encounter")
        self.assertEqual(action["target"], "new")
        return action["res_id"]

    def test_start_visit_blocked_when_readiness_incomplete(self):
        appointment = self._create_appointment()

        self.assertEqual(appointment.visit_status, "scheduled")
        self.assertEqual(
            self.env["hc.encounter"].search_count([("appointment_id", "=", appointment.id)]),
            0,
        )

        with self.assertRaisesRegex(
            UserError,
            "Intake and consent must both be complete before starting the visit.",
        ):
            appointment.action_start_visit()

        appointment.invalidate_recordset(["visit_status"])
        self.assertEqual(appointment.visit_status, "scheduled")
        self.assertEqual(
            self.env["hc.encounter"].search_count([("appointment_id", "=", appointment.id)]),
            0,
        )

    def test_start_visit_sets_in_progress_and_opens_encounter(self):
        appointment = self._create_appointment()
        self._create_complete_readiness(appointment)

        first_action = appointment.action_start_visit()
        appointment.invalidate_recordset(["visit_status"])
        first_res_id = self._assert_encounter_action(first_action)

        self.assertEqual(appointment.visit_status, "in_progress")
        self.assertEqual(
            self.env["hc.encounter"].search_count([("appointment_id", "=", appointment.id)]),
            1,
        )

        second_action = appointment.action_start_visit()
        second_res_id = self._assert_encounter_action(second_action)

        self.assertEqual(first_res_id, second_res_id)
        self.assertEqual(
            self.env["hc.encounter"].search_count([("appointment_id", "=", appointment.id)]),
            1,
        )

    def test_complete_visit_requires_encounter(self):
        appointment = self._create_appointment()

        self.assertEqual(appointment.visit_status, "scheduled")

        with self.assertRaisesRegex(
            UserError,
            "An encounter is required before completing the visit.",
        ):
            appointment.action_complete_visit()

        appointment.invalidate_recordset(["visit_status"])
        self.assertEqual(appointment.visit_status, "scheduled")

    def test_complete_visit_sets_completed_and_completes_encounter(self):
        appointment = self._create_appointment()
        encounter_action = appointment.action_open_encounter()
        encounter = self.env["hc.encounter"].browse(
            self._assert_encounter_action(encounter_action)
        )

        self.assertEqual(encounter.status, "draft")
        self.assertFalse(encounter.completed_on)

        result = appointment.action_complete_visit()

        self.assertTrue(result)
        appointment.invalidate_recordset(["visit_status"])
        encounter.invalidate_recordset(["status", "completed_on"])
        self.assertEqual(appointment.visit_status, "completed")
        self.assertEqual(encounter.status, "complete")
        self.assertTrue(encounter.completed_on)

    def test_close_visit_blocked_unless_completed(self):
        appointment = self._create_appointment()

        self.assertEqual(appointment.visit_status, "scheduled")

        with self.assertRaisesRegex(UserError, "Only completed visits can be closed."):
            appointment.action_close_visit()

        appointment.invalidate_recordset(["visit_status"])
        self.assertEqual(appointment.visit_status, "scheduled")

    def test_close_visit_sets_closed_without_changing_encounter(self):
        appointment = self._create_appointment()
        encounter_action = appointment.action_open_encounter()
        encounter = self.env["hc.encounter"].browse(
            self._assert_encounter_action(encounter_action)
        )

        appointment.action_complete_visit()
        encounter.invalidate_recordset(["status", "completed_on"])
        completed_on = encounter.completed_on

        self.assertEqual(encounter.status, "complete")
        self.assertTrue(completed_on)

        result = appointment.action_close_visit()

        self.assertTrue(result)
        appointment.invalidate_recordset(["visit_status"])
        encounter.invalidate_recordset(["status", "completed_on"])
        self.assertEqual(appointment.visit_status, "closed")
        self.assertEqual(encounter.status, "complete")
        self.assertEqual(encounter.completed_on, completed_on)

    def test_follow_up_blocked_unless_closed(self):
        appointment = self._create_appointment()

        self.assertFalse(appointment.needs_follow_up)

        with self.assertRaisesRegex(
            UserError,
            "Follow-up can only be managed after the visit is closed.",
        ):
            appointment.action_mark_needs_follow_up()

        with self.assertRaisesRegex(
            UserError,
            "Follow-up can only be managed after the visit is closed.",
        ):
            appointment.action_clear_follow_up()

        appointment.invalidate_recordset(["needs_follow_up"])
        self.assertFalse(appointment.needs_follow_up)

    def test_mark_and_clear_follow_up_after_closed(self):
        appointment = self._create_appointment()
        encounter_action = appointment.action_open_encounter()
        encounter = self.env["hc.encounter"].browse(
            self._assert_encounter_action(encounter_action)
        )

        appointment.action_complete_visit()
        appointment.action_close_visit()
        encounter.invalidate_recordset(["status", "completed_on"])
        initial_status = encounter.status
        initial_completed_on = encounter.completed_on

        self.assertEqual(initial_status, "complete")
        self.assertTrue(initial_completed_on)

        appointment.action_mark_needs_follow_up()
        appointment.invalidate_recordset(["needs_follow_up"])
        encounter.invalidate_recordset(["status", "completed_on"])
        self.assertTrue(appointment.needs_follow_up)
        self.assertEqual(encounter.status, initial_status)
        self.assertEqual(encounter.completed_on, initial_completed_on)

        appointment.action_clear_follow_up()
        appointment.invalidate_recordset(["needs_follow_up"])
        encounter.invalidate_recordset(["status", "completed_on"])
        self.assertFalse(appointment.needs_follow_up)
        self.assertEqual(encounter.status, initial_status)
        self.assertEqual(encounter.completed_on, initial_completed_on)
