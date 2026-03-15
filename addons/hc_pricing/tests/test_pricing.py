from datetime import timedelta

from odoo import fields
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestPricing(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.practice = cls.env["hc.practice"].create({"name": "Pricing Test Practice"})
        cls.other_practice = cls.env["hc.practice"].create({"name": "Other Pricing Practice"})
        cls.patient = cls.env["res.partner"].create(
            {
                "name": "Pricing Test Patient",
                "is_hc_patient": True,
                "practice_id": cls.practice.id,
            }
        )
        cls.practitioner = cls.env["hc.practitioner"].create(
            {
                "name": "Pricing Test Practitioner",
                "practice_id": cls.practice.id,
            }
        )
        cls.appointment_type = cls.env["hc.appointment.type"].create(
            {
                "name": "Pricing Test Visit",
                "practice_id": cls.practice.id,
            }
        )
        cls.other_appointment_type = cls.env["hc.appointment.type"].create(
            {
                "name": "Other Pricing Visit",
                "practice_id": cls.other_practice.id,
            }
        )
        cls.default_fee = cls.env["hc.service.fee"].create(
            {
                "name": "Initial Acupuncture Visit",
                "practice_id": cls.practice.id,
                "default_price": 135.0,
                "short_description": "First-visit fee",
            }
        )
        cls.alternate_fee = cls.env["hc.service.fee"].create(
            {
                "name": "Follow-Up Acupuncture Visit",
                "practice_id": cls.practice.id,
                "default_price": 95.0,
            }
        )
        cls.other_fee = cls.env["hc.service.fee"].create(
            {
                "name": "Other Practice Fee",
                "practice_id": cls.other_practice.id,
                "default_price": 88.0,
            }
        )
        cls.front_desk_user = cls.env["res.users"].with_context(
            no_reset_password=True
        ).create(
            {
                "name": "Pricing Front Desk",
                "login": "pricing_front_desk",
                "email": "pricing_front_desk@example.com",
                "practice_id": cls.practice.id,
                "group_ids": [
                    (
                        6,
                        0,
                        [
                            cls.env.ref("base.group_user").id,
                            cls.env.ref("hc_practice_core.hc_group_front_desk").id,
                        ],
                    )
                ],
            }
        )

    def _create_appointment(self, appointment_type=None, visit_status="closed"):
        appointment_type = appointment_type or self.appointment_type
        start_datetime = fields.Datetime.now()
        return self.env["hc.appointment"].create(
            {
                "patient_id": self.patient.id,
                "practitioner_id": self.practitioner.id,
                "practice_id": self.practice.id,
                "appointment_type_id": appointment_type.id,
                "start_datetime": start_datetime,
                "end_datetime": start_datetime + timedelta(hours=1),
                "visit_status": visit_status,
            }
        )

    def test_service_fee_rejects_negative_price(self):
        with self.assertRaisesRegex(
            ValidationError,
            "Service fee default price must be zero or greater.",
        ):
            self.env["hc.service.fee"].create(
                {
                    "name": "Negative Fee",
                    "practice_id": self.practice.id,
                    "default_price": -1.0,
                }
            )

    def test_appointment_type_rejects_cross_practice_default_fee(self):
        with self.assertRaisesRegex(
            ValidationError,
            "Default service fee must belong to the same practice as the appointment type.",
        ):
            self.other_appointment_type.write(
                {
                    "default_service_fee_id": self.default_fee.id,
                }
            )

    def test_start_checkout_prefills_from_default_service_fee(self):
        self.appointment_type.default_service_fee_id = self.default_fee
        appointment = self._create_appointment()

        action = appointment.action_start_checkout()
        session = self.env["hc.checkout.session"].browse(action["res_id"])
        line = session.checkout_line_ids[:1]

        self.assertEqual(session.service_fee_id, self.default_fee)
        self.assertEqual(session.charge_label, self.default_fee.name)
        self.assertEqual(session.amount_total, self.default_fee.default_price)
        self.assertEqual(line.service_fee_id, self.default_fee)
        self.assertEqual(line.description, self.default_fee.name)
        self.assertEqual(line.amount, self.default_fee.default_price)

    def test_start_checkout_preserves_sprint7_fallback_without_default_fee(self):
        appointment = self._create_appointment()

        action = appointment.action_start_checkout()
        session = self.env["hc.checkout.session"].browse(action["res_id"])
        line = session.checkout_line_ids[:1]

        self.assertFalse(session.service_fee_id)
        self.assertEqual(session.charge_label, appointment.appointment_type_id.display_name)
        self.assertEqual(session.amount_total, 0.0)
        self.assertFalse(line.service_fee_id)
        self.assertEqual(line.description, appointment.appointment_type_id.display_name)
        self.assertEqual(line.amount, 0.0)

    def test_open_checkout_fee_selection_refreshes_defaults(self):
        appointment = self._create_appointment()
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Manual Default",
                "amount_total": 0.0,
            }
        )
        line = session.checkout_line_ids[:1]

        line.write({"service_fee_id": self.alternate_fee.id})

        session.invalidate_recordset(["service_fee_id", "charge_label", "amount_total"])
        line.invalidate_recordset(["service_fee_id", "description", "amount"])
        self.assertEqual(session.service_fee_id, self.alternate_fee)
        self.assertEqual(session.charge_label, self.alternate_fee.name)
        self.assertEqual(session.amount_total, self.alternate_fee.default_price)
        self.assertEqual(line.service_fee_id, self.alternate_fee)
        self.assertEqual(line.description, self.alternate_fee.name)
        self.assertEqual(line.amount, self.alternate_fee.default_price)

    def test_service_fee_selection_preserves_explicit_manual_values(self):
        appointment = self._create_appointment()
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Original Charge",
                "amount_total": 50.0,
            }
        )
        line = session.checkout_line_ids[:1]

        line.write(
            {
                "service_fee_id": self.default_fee.id,
                "description": "Custom Front Desk Charge",
                "amount": 111.0,
            }
        )

        session.invalidate_recordset(["service_fee_id", "charge_label", "amount_total"])
        line.invalidate_recordset(["service_fee_id", "description", "amount"])
        self.assertEqual(session.service_fee_id, self.default_fee)
        self.assertEqual(session.charge_label, "Custom Front Desk Charge")
        self.assertEqual(session.amount_total, 111.0)
        self.assertEqual(line.description, "Custom Front Desk Charge")
        self.assertEqual(line.amount, 111.0)

    def test_existing_checkout_values_remain_stable_when_fee_changes_later(self):
        self.appointment_type.default_service_fee_id = self.default_fee
        appointment = self._create_appointment()
        action = appointment.action_start_checkout()
        session = self.env["hc.checkout.session"].browse(action["res_id"])
        line = session.checkout_line_ids[:1]

        self.default_fee.write(
            {
                "name": "Renamed Initial Visit",
                "default_price": 150.0,
            }
        )

        session.invalidate_recordset(["service_fee_id", "charge_label", "amount_total"])
        line.invalidate_recordset(["service_fee_id", "description", "amount"])
        self.assertEqual(session.service_fee_id, self.default_fee)
        self.assertEqual(session.charge_label, "Initial Acupuncture Visit")
        self.assertEqual(session.amount_total, 135.0)
        self.assertEqual(line.description, "Initial Acupuncture Visit")
        self.assertEqual(line.amount, 135.0)

    def test_service_fee_must_match_checkout_practice(self):
        appointment = self._create_appointment()
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Visit Charge",
                "amount_total": 100.0,
            }
        )
        line = session.checkout_line_ids[:1]

        with self.assertRaisesRegex(
            ValidationError,
            "Service fee must belong to the same practice as the appointment.",
        ):
            line.write({"service_fee_id": self.other_fee.id})

    def test_service_fee_change_is_blocked_when_checkout_not_open(self):
        appointment = self._create_appointment()
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Visit Charge",
                "amount_total": 100.0,
            }
        )
        line = session.checkout_line_ids[:1]
        session.action_mark_payment_due()

        with self.assertRaisesRegex(
            UserError,
            "Checkout lines can only be changed while checkout is open.",
        ):
            line.write({"service_fee_id": self.default_fee.id})

    def test_front_desk_can_read_fee_but_cannot_manage_fee_config(self):
        fee_read = self.default_fee.with_user(self.front_desk_user).name
        self.assertEqual(fee_read, self.default_fee.name)

        with self.assertRaises(AccessError):
            self.env["hc.service.fee"].with_user(self.front_desk_user).create(
                {
                    "name": "Front Desk Fee",
                    "practice_id": self.practice.id,
                    "default_price": 45.0,
                }
            )

    def test_front_desk_can_apply_service_fee_to_open_checkout(self):
        appointment = self._create_appointment()
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Visit Charge",
                "amount_total": 100.0,
            }
        )
        line = session.checkout_line_ids[:1]

        line.with_user(self.front_desk_user).write({"service_fee_id": self.default_fee.id})

        session.invalidate_recordset(["service_fee_id", "charge_label", "amount_total"])
        line.invalidate_recordset(["service_fee_id", "description", "amount"])
        self.assertEqual(session.service_fee_id, self.default_fee)
        self.assertEqual(session.charge_label, self.default_fee.name)
        self.assertEqual(session.amount_total, self.default_fee.default_price)
        self.assertEqual(line.service_fee_id, self.default_fee)
        self.assertEqual(line.description, self.default_fee.name)
        self.assertEqual(line.amount, self.default_fee.default_price)
