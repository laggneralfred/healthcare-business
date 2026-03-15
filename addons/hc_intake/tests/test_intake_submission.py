from datetime import timedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestIntakeSubmission(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.practice = cls.env["hc.practice"].create(
            {
                "name": "Intake Test Practice",
            }
        )
        cls.patient = cls.env["res.partner"].create(
            {
                "name": "Intake Test Patient",
                "is_hc_patient": True,
                "practice_id": cls.practice.id,
            }
        )
        cls.practitioner = cls.env["hc.practitioner"].create(
            {
                "name": "Intake Test Practitioner",
                "practice_id": cls.practice.id,
            }
        )
        cls.appointment_type = cls.env["hc.appointment.type"].create(
            {
                "name": "Intake Test Visit",
                "practice_id": cls.practice.id,
            }
        )
        cls.template = cls.env["hc.intake.template"].create(
            {
                "name": "Intake Test Template",
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

    def _create_submission(self, appointment=False):
        return self.env["hc.intake.submission"].create(
            {
                "patient_id": self.patient.id,
                "practice_id": self.practice.id,
                "appointment_id": appointment.id if appointment else False,
                "template_id": self.template.id,
                "status": "missing",
                "submitted_on": False,
            }
        )

    def test_public_submit_marks_complete_and_sets_submitted_on(self):
        appointment = self._create_appointment()
        submission = self._create_submission(appointment=appointment)

        submission.action_submit_public_intake(
            {
                "reason_for_visit": "Annual wellness visit",
                "notes": "Patient completed this from the public token flow",
            }
        )

        self.assertEqual(submission.status, "complete")
        self.assertTrue(submission.submitted_on)
        self.assertEqual(submission.patient_id, self.patient)
        self.assertEqual(submission.practice_id, self.practice)
        self.assertEqual(submission.appointment_id, appointment)

    def test_public_submit_empty_payload_is_rejected(self):
        submission = self._create_submission()

        with self.assertRaisesRegex(
            ValidationError,
            "Complete intake records must include at least one intake content field.",
        ):
            submission.action_submit_public_intake({})

        self.assertEqual(submission.status, "missing")
        self.assertFalse(submission.submitted_on)

    def test_access_token_is_generated_and_stable(self):
        submission = self._create_submission()

        self.assertFalse(submission.access_token)

        first_token = submission._ensure_access_token()
        second_token = submission._ensure_access_token()

        self.assertTrue(first_token)
        self.assertEqual(first_token, submission.access_token)
        self.assertEqual(second_token, first_token)
