from datetime import timedelta

from odoo import fields
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestCheckoutSession(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.practice = cls.env["hc.practice"].create(
            {
                "name": "Checkout Test Practice",
            }
        )
        cls.patient = cls.env["res.partner"].create(
            {
                "name": "Checkout Test Patient",
                "is_hc_patient": True,
                "practice_id": cls.practice.id,
            }
        )
        cls.practitioner = cls.env["hc.practitioner"].create(
            {
                "name": "Checkout Test Practitioner",
                "practice_id": cls.practice.id,
            }
        )
        cls.appointment_type = cls.env["hc.appointment.type"].create(
            {
                "name": "Checkout Test Visit",
                "practice_id": cls.practice.id,
            }
        )
        cls.front_desk_user = cls.env["res.users"].with_context(
            no_reset_password=True
        ).create(
            {
                "name": "Checkout Front Desk",
                "login": "checkout_front_desk",
                "email": "checkout_front_desk@example.com",
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
        cls.provider_user = cls.env["res.users"].with_context(
            no_reset_password=True
        ).create(
            {
                "name": "Checkout Provider",
                "login": "checkout_provider",
                "email": "checkout_provider@example.com",
                "practice_id": cls.practice.id,
                "group_ids": [
                    (
                        6,
                        0,
                        [
                            cls.env.ref("base.group_user").id,
                            cls.env.ref("hc_practice_core.hc_group_provider").id,
                        ],
                    )
                ],
            }
        )

    def _create_appointment(self, visit_status="scheduled", needs_follow_up=False):
        start_datetime = fields.Datetime.now()
        return self.env["hc.appointment"].create(
            {
                "patient_id": self.patient.id,
                "practitioner_id": self.practitioner.id,
                "practice_id": self.practice.id,
                "appointment_type_id": self.appointment_type.id,
                "start_datetime": start_datetime,
                "end_datetime": start_datetime + timedelta(hours=1),
                "visit_status": visit_status,
                "needs_follow_up": needs_follow_up,
            }
        )

    def _assert_checkout_action(self, action):
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "hc.checkout.session")
        return action["res_id"]

    def test_start_checkout_blocked_unless_closed(self):
        appointment = self._create_appointment()

        with self.assertRaisesRegex(
            UserError,
            "Checkout can only be started after the visit is closed.",
        ):
            appointment.action_start_checkout()

        self.assertEqual(
            self.env["hc.checkout.session"].search_count([("appointment_id", "=", appointment.id)]),
            0,
        )

    def test_start_checkout_creates_session_and_updates_summary(self):
        appointment = self._create_appointment(visit_status="closed")

        action = appointment.action_start_checkout()
        session = self.env["hc.checkout.session"].browse(self._assert_checkout_action(action))

        self.assertTrue(session.exists())
        self.assertEqual(session.appointment_id, appointment)
        self.assertEqual(session.patient_id, appointment.patient_id)
        self.assertEqual(session.practitioner_id, appointment.practitioner_id)
        self.assertEqual(session.appointment_start, appointment.start_datetime)
        self.assertEqual(session.state, "open")
        self.assertEqual(session.charge_label, appointment.appointment_type_id.display_name)
        self.assertEqual(session.amount_total, 0.0)
        self.assertTrue(session.started_on)
        self.assertEqual(len(session.checkout_line_ids), 1)
        self.assertEqual(session.checkout_line_ids.description, appointment.appointment_type_id.display_name)
        self.assertEqual(session.checkout_line_ids.amount, 0.0)

        appointment.invalidate_recordset(
            [
                "checkout_session_id",
                "checkout_status",
                "checkout_amount_total",
                "checkout_tender_type",
                "checkout_paid_on",
            ]
        )
        self.assertEqual(appointment.checkout_session_id, session)
        self.assertEqual(appointment.checkout_status, "open")
        self.assertEqual(appointment.checkout_amount_total, 0.0)
        self.assertFalse(appointment.checkout_tender_type)
        self.assertFalse(appointment.checkout_paid_on)

    def test_start_checkout_reopens_existing_session(self):
        appointment = self._create_appointment(visit_status="closed")

        first_action = appointment.action_start_checkout()
        second_action = appointment.action_start_checkout()

        first_session = self.env["hc.checkout.session"].browse(
            self._assert_checkout_action(first_action)
        )
        second_session = self.env["hc.checkout.session"].browse(
            self._assert_checkout_action(second_action)
        )

        self.assertEqual(first_session, second_session)
        self.assertEqual(
            self.env["hc.checkout.session"].search_count([("appointment_id", "=", appointment.id)]),
            1,
        )

    def test_checkout_creation_requires_closed_appointment(self):
        appointment = self._create_appointment()

        with self.assertRaisesRegex(
            ValidationError,
            "Checkout can only be created for closed appointments.",
        ):
            self.env["hc.checkout.session"].create(
                {
                    "appointment_id": appointment.id,
                    "charge_label": "Scheduled Visit",
                }
            )

    def test_mark_cash_paid_sets_paid_state_and_preserves_appointment(self):
        appointment = self._create_appointment(visit_status="closed", needs_follow_up=True)
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Visit Charge",
                "amount_total": 125.0,
            }
        )

        result = session.action_mark_cash_paid()

        self.assertTrue(result)
        session.invalidate_recordset(["state", "tender_type", "amount_paid", "paid_on"])
        appointment.invalidate_recordset(
            [
                "visit_status",
                "needs_follow_up",
                "checkout_status",
                "checkout_tender_type",
                "checkout_paid_on",
                "checkout_amount_total",
            ]
        )
        self.assertEqual(session.state, "paid")
        self.assertEqual(session.tender_type, "cash")
        self.assertEqual(session.amount_paid, 125.0)
        self.assertTrue(session.paid_on)
        self.assertEqual(appointment.visit_status, "closed")
        self.assertTrue(appointment.needs_follow_up)
        self.assertEqual(appointment.checkout_status, "paid")
        self.assertEqual(appointment.checkout_tender_type, "cash")
        self.assertEqual(appointment.checkout_amount_total, 125.0)
        self.assertEqual(appointment.checkout_paid_on, session.paid_on)

    def test_mark_card_paid_sets_paid_state(self):
        appointment = self._create_appointment(visit_status="closed")
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Visit Charge",
                "amount_total": 95.0,
            }
        )

        result = session.action_mark_card_paid()

        self.assertTrue(result)
        session.invalidate_recordset(["state", "tender_type", "amount_paid", "paid_on"])
        appointment.invalidate_recordset(["checkout_status", "checkout_tender_type"])
        self.assertEqual(session.state, "paid")
        self.assertEqual(session.tender_type, "card")
        self.assertEqual(session.amount_paid, 95.0)
        self.assertTrue(session.paid_on)
        self.assertEqual(appointment.checkout_status, "paid")
        self.assertEqual(appointment.checkout_tender_type, "card")

    def test_mark_payment_due_sets_due_state_without_payment_details(self):
        appointment = self._create_appointment(visit_status="closed", needs_follow_up=True)
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Visit Charge",
                "amount_total": 140.0,
            }
        )

        result = session.action_mark_payment_due()

        self.assertTrue(result)
        session.invalidate_recordset(["state", "tender_type", "amount_paid", "paid_on"])
        appointment.invalidate_recordset(
            ["visit_status", "needs_follow_up", "checkout_status", "checkout_tender_type"]
        )
        self.assertEqual(session.state, "payment_due")
        self.assertFalse(session.tender_type)
        self.assertEqual(session.amount_paid, 0.0)
        self.assertFalse(session.paid_on)
        self.assertEqual(appointment.visit_status, "closed")
        self.assertTrue(appointment.needs_follow_up)
        self.assertEqual(appointment.checkout_status, "payment_due")
        self.assertFalse(appointment.checkout_tender_type)

    def test_payment_actions_are_blocked_once_session_is_not_open(self):
        appointment = self._create_appointment(visit_status="closed")
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Visit Charge",
                "amount_total": 80.0,
            }
        )
        session.action_mark_payment_due()

        with self.assertRaisesRegex(
            UserError,
            "Only open checkout sessions can be updated.",
        ):
            session.action_mark_cash_paid()

    def test_front_desk_can_start_checkout(self):
        appointment = self._create_appointment(visit_status="closed")

        action = appointment.with_user(self.front_desk_user).action_start_checkout()
        session = self.env["hc.checkout.session"].browse(self._assert_checkout_action(action))

        self.assertTrue(session.exists())
        self.assertEqual(session.appointment_id, appointment)

    def test_provider_cannot_update_checkout_session(self):
        appointment = self._create_appointment(visit_status="closed")
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Visit Charge",
                "amount_total": 100.0,
            }
        )

        with self.assertRaises(AccessError):
            session.with_user(self.provider_user).action_mark_cash_paid()

    def test_checkout_lines_update_amount_total(self):
        appointment = self._create_appointment(visit_status="closed")
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Base Visit Charge",
                "amount_total": 100.0,
            }
        )

        self.env["hc.checkout.line"].create(
            {
                "checkout_session_id": session.id,
                "sequence": 20,
                "description": "Extra Service",
                "amount": 25.0,
            }
        )

        session.invalidate_recordset(["amount_total"])
        self.assertEqual(session.amount_total, 125.0)

    def test_checkout_line_changes_blocked_when_session_not_open(self):
        appointment = self._create_appointment(visit_status="closed")
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Visit Charge",
                "amount_total": 80.0,
            }
        )
        line = session.checkout_line_ids[:1]
        session.action_mark_payment_due()

        with self.assertRaisesRegex(
            UserError,
            "Checkout lines can only be changed while checkout is open.",
        ):
            line.write({"amount": 90.0})

    def test_checkout_line_resequence_and_delete_update_total(self):
        appointment = self._create_appointment(visit_status="closed")
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Visit Charge",
                "amount_total": 60.0,
            }
        )
        first_line = session.checkout_line_ids[:1]
        second_line = self.env["hc.checkout.line"].create(
            {
                "checkout_session_id": session.id,
                "sequence": 20,
                "description": "Supplemental Charge",
                "amount": 40.0,
            }
        )

        second_line.write({"sequence": 5})
        session.invalidate_recordset(["amount_total", "charge_label"])
        self.assertEqual(session.amount_total, 100.0)
        self.assertEqual(session.charge_label, "Supplemental Charge")

        first_line.unlink()
        session.invalidate_recordset(["amount_total", "charge_label"])
        self.assertEqual(session.amount_total, 40.0)
        self.assertEqual(session.charge_label, "Supplemental Charge")

    def test_checkout_line_rejects_negative_amount(self):
        appointment = self._create_appointment(visit_status="closed")
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Visit Charge",
            }
        )

        with self.assertRaisesRegex(
            ValidationError,
            "Checkout line amount must be zero or greater.",
        ):
            self.env["hc.checkout.line"].create(
                {
                    "checkout_session_id": session.id,
                    "description": "Bad Charge",
                    "amount": -1.0,
                }
            )

    def test_backfill_creates_default_line_for_existing_session(self):
        appointment = self._create_appointment(visit_status="closed")
        session = self.env["hc.checkout.session"].with_context(
            skip_default_line_creation=True
        ).create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Legacy Charge",
                "amount_total": 77.0,
            }
        )

        self.assertFalse(session.checkout_line_ids)

        self.env["hc.checkout.session"]._backfill_missing_checkout_lines()
        session.invalidate_recordset(["checkout_line_ids", "amount_total", "charge_label"])

        self.assertEqual(len(session.checkout_line_ids), 1)
        self.assertEqual(session.checkout_line_ids.description, "Legacy Charge")
        self.assertEqual(session.checkout_line_ids.amount, 77.0)

    def test_checkout_summary_report_renders_session_context(self):
        appointment = self._create_appointment(visit_status="closed")
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Visit Charge",
                "amount_total": 60.0,
            }
        )
        self.env["hc.checkout.line"].create(
            {
                "checkout_session_id": session.id,
                "sequence": 20,
                "description": "Supplemental Charge",
                "amount": 15.0,
            }
        )

        report = self.env.ref("hc_checkout.action_report_hc_checkout_summary")
        html, _ = report._render_qweb_html(report.report_name, session.ids)
        rendered = html.decode()

        self.assertIn("Checkout Summary", rendered)
        self.assertIn(self.practice.name, rendered)
        self.assertIn(self.patient.name, rendered)
        self.assertIn(appointment.display_name, rendered)
        self.assertIn("Visit Charge", rendered)
        self.assertIn("Supplemental Charge", rendered)
        self.assertIn("75.00", rendered)
        self.assertIn("Open", rendered)

    def test_paid_checkout_summary_report_shows_tender_for_front_desk(self):
        appointment = self._create_appointment(visit_status="closed")
        session = self.env["hc.checkout.session"].create(
            {
                "appointment_id": appointment.id,
                "charge_label": "Visit Charge",
                "amount_total": 90.0,
            }
        )
        session.action_mark_card_paid()

        report = self.env.ref("hc_checkout.action_report_hc_checkout_summary").with_user(
            self.front_desk_user
        )
        html, _ = report._render_qweb_html(report.report_name, session.ids)
        rendered = html.decode()

        self.assertIn("Paid", rendered)
        self.assertIn("Card", rendered)
        self.assertIn("90.00", rendered)
