{
    "name": "Healthcare Pricing",
    "summary": "Sprint 8 minimal structured pricing defaults",
    "version": "19.0.1.0.0",
    "category": "Healthcare",
    "author": "Codex",
    "license": "LGPL-3",
    "depends": [
        "base",
        "hc_practice_core",
        "hc_scheduling",
        "hc_checkout",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hc_service_fee_views.xml",
        "views/hc_appointment_type_views.xml",
        "views/hc_checkout_views.xml",
        "views/hc_pricing_menus.xml",
    ],
    "installable": True,
    "application": False,
}
