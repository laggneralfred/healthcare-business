{
    "name": "Healthcare Encounter",
    "summary": "Sprint 3 encounter foundation",
    "version": "19.0.1.0.0",
    "category": "Healthcare",
    "author": "Codex",
    "license": "LGPL-3",
    "depends": [
        "base",
        "hc_practice_core",
        "hc_patient_core",
        "hc_scheduling",
        "hc_intake",
        "hc_consent",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hc_encounter_views.xml",
        "views/hc_encounter_appointment_views.xml",
    ],
    "installable": True,
    "application": False,
}
