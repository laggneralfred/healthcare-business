import json


PASSWORD = "SmokePass123!"


def ensure_user(env, *, login, name, practice, groups):
    users = env["res.users"].sudo().with_context(no_reset_password=True)
    user = users.search([("login", "=", login)], limit=1)
    vals = {
        "name": name,
        "login": login,
        "email": f"{login}@example.com",
        "practice_id": practice.id,
        "group_ids": [(6, 0, [env.ref("base.group_user").id, *groups.ids])],
    }
    if user:
        user.write(vals)
    else:
        user = users.create(vals)
    user.write({"password": PASSWORD})
    return user


def ensure_record(model, domain, vals):
    record = model.search(domain, limit=1)
    if record:
        record.write(vals)
    else:
        record = model.create(vals)
    return record


practice_model = env["hc.practice"].sudo()
patient_model = env["res.partner"].sudo()
practitioner_model = env["hc.practitioner"].sudo()
appointment_type_model = env["hc.appointment.type"].sudo()
appointment_model = env["hc.appointment"].sudo()
service_fee_model = env["hc.service.fee"].sudo()
checkout_model = env["hc.checkout.session"].sudo()

group_owner = env.ref("hc_practice_core.hc_group_owner")
group_front_desk = env.ref("hc_practice_core.hc_group_front_desk")
group_provider = env.ref("hc_practice_core.hc_group_provider")

practice = ensure_record(
    practice_model,
    [("name", "=", "Smoke Clinic")],
    {
        "name": "Smoke Clinic",
        "timezone": "America/Los_Angeles",
        "active": True,
    },
)

owner_user = ensure_user(
    env,
    login="smoke.owner",
    name="Smoke Owner",
    practice=practice,
    groups=group_owner,
)
front_desk_user = ensure_user(
    env,
    login="smoke.frontdesk",
    name="Smoke Front Desk",
    practice=practice,
    groups=group_front_desk,
)
provider_user = ensure_user(
    env,
    login="smoke.provider",
    name="Smoke Provider",
    practice=practice,
    groups=group_provider,
)

service_fee = ensure_record(
    service_fee_model,
    [("name", "=", "Smoke Initial Visit Fee"), ("practice_id", "=", practice.id)],
    {
        "name": "Smoke Initial Visit Fee",
        "practice_id": practice.id,
        "default_price": 120.0,
        "short_description": "Pilot smoke default fee",
        "active": True,
    },
)

appointment_type = ensure_record(
    appointment_type_model,
    [("name", "=", "Smoke Initial Visit"), ("practice_id", "=", practice.id)],
    {
        "name": "Smoke Initial Visit",
        "practice_id": practice.id,
        "default_service_fee_id": service_fee.id,
        "active": True,
    },
)

practitioner = ensure_record(
    practitioner_model,
    [("name", "=", "Smoke Provider Practitioner"), ("practice_id", "=", practice.id)],
    {
        "name": "Smoke Provider Practitioner",
        "practice_id": practice.id,
        "active": True,
    },
)

patient = ensure_record(
    patient_model,
    [("name", "=", "Smoke Patient"), ("practice_id", "=", practice.id)],
    {
        "name": "Smoke Patient",
        "is_hc_patient": True,
        "practice_id": practice.id,
        "phone": "555-0100",
        "email": "smoke.patient@example.com",
    },
)

existing_appointments = appointment_model.search(
    [("notes", "=", "PLAYWRIGHT_SMOKE_APPOINTMENT"), ("practice_id", "=", practice.id)]
)
if existing_appointments:
    existing_appointments.unlink()

appointment = appointment_model.create(
    {
        "patient_id": patient.id,
        "practitioner_id": practitioner.id,
        "practice_id": practice.id,
        "appointment_type_id": appointment_type.id,
        "start_datetime": "2026-03-18 16:00:00",
        "end_datetime": "2026-03-18 17:00:00",
        "visit_status": "closed",
        "notes": "PLAYWRIGHT_SMOKE_APPOINTMENT",
    }
)

data = {
    "base_url": "http://127.0.0.1:8069",
    "users": {
        "owner": {"login": owner_user.login, "password": PASSWORD},
        "front_desk": {"login": front_desk_user.login, "password": PASSWORD},
        "provider": {"login": provider_user.login, "password": PASSWORD},
    },
    "actions": {
        "patients": "hc_patient_core.action_hc_patients",
        "appointments": "hc_scheduling.action_hc_appointments",
        "checkout": "hc_checkout.action_hc_checkout_sessions",
        "service_fees": "hc_pricing.action_hc_service_fees",
    },
    "records": {
        "practice_id": practice.id,
        "patient_id": patient.id,
        "appointment_id": appointment.id,
        "appointment_type_id": appointment_type.id,
        "service_fee_id": service_fee.id,
    },
    "expected": {
        "service_fee_name": service_fee.name,
        "appointment_type_name": appointment_type.name,
        "patient_name": patient.name,
        "appointment_name": appointment.display_name,
        "checkout_name": f"CHK/{appointment.id}",
        "checkout_total": "120.00",
    },
}

env.cr.commit()
print(json.dumps(data, indent=2))
