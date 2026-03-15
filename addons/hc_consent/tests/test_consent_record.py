from datetime import timedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestConsentRecord(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.practice = cls.env["hc.practice"].create(
            {
                "name": "Consent Test Practice",
            }
        )
        cls.patient = cls.env["res.partner"].create(
            {
                "name": "Consent Test Patient",
                "is_hc_patient": True,
                "practice_id": cls.practice.id,
            }
        )
        cls.practitioner = cls.env["hc.practitioner"].create(
            {
                "name": "Consent Test Practitioner",
                "practice_id": cls.practice.id,
            }
        )
        cls.appointment_type = cls.env["hc.appointment.type"].create(
            {
                "name": "Consent Test Visit",
                "practice_id": cls.practice.id,
            }
        )
        cls.template = cls.env["hc.consent.template"].create(
            {
                "name": "Consent Test Template",
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

    def _create_record(self, appointment=False):
        return self.env["hc.consent.record"].create(
            {
                "patient_id": self.patient.id,
                "practice_id": self.practice.id,
                "appointment_id": appointment.id if appointment else False,
                "template_id": self.template.id,
                "status": "missing",
                "signed_on": False,
            }
        )

    def test_public_submit_marks_complete_and_sets_signed_on(self):
        appointment = self._create_appointment()
        record = self._create_record(appointment=appointment)

        record.action_submit_public_consent(
            {
                "consent_given_by": "Consent Test Patient",
                "notes": "Patient completed this from the public token flow",
            }
        )

        self.assertEqual(record.status, "complete")
        self.assertTrue(record.signed_on)
        self.assertEqual(record.patient_id, self.patient)
        self.assertEqual(record.practice_id, self.practice)
        self.assertEqual(record.appointment_id, appointment)

    def test_public_submit_empty_payload_is_rejected(self):
        record = self._create_record()

        with self.assertRaisesRegex(
            ValidationError,
            "Complete consent records must include at least one consent content field.",
        ):
            record.action_submit_public_consent({})

        self.assertEqual(record.status, "missing")
        self.assertFalse(record.signed_on)

    def test_access_token_is_generated_and_stable(self):
        record = self._create_record()

        self.assertFalse(record.access_token)

        first_token = record._ensure_access_token()
        second_token = record._ensure_access_token()

        self.assertTrue(first_token)
        self.assertEqual(first_token, record.access_token)
        self.assertEqual(second_token, first_token)
