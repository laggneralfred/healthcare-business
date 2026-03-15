{
    "name": "Healthcare Scheduling",
    "summary": "Sprint 1 appointment scheduling foundation",
    "version": "19.0.1.0.0",
    "category": "Healthcare",
    "author": "Codex",
    "license": "LGPL-3",
    "depends": [
        "base",
        "calendar",
        "hc_practice_core",
        "hc_patient_core",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hc_practitioner_views.xml",
        "views/hc_appointment_type_views.xml",
        "views/hc_appointment_views.xml",
        "views/hc_scheduling_menus.xml",
    ],
    "installable": True,
    "application": False,
}
