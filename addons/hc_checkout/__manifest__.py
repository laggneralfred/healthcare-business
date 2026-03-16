{
    "name": "Healthcare Checkout",
    "summary": "Sprint 7 minimal self-pay checkout",
    "version": "19.0.1.0.0",
    "category": "Healthcare",
    "author": "Codex",
    "license": "LGPL-3",
    "depends": [
        "base",
        "hc_practice_core",
        "hc_patient_core",
        "hc_scheduling",
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/hc_checkout_summary_report.xml",
        "views/hc_checkout_views.xml",
        "views/hc_checkout_appointment_views.xml",
        "views/hc_checkout_patient_views.xml",
        "views/hc_checkout_menus.xml",
    ],
    "installable": True,
    "application": False,
}
