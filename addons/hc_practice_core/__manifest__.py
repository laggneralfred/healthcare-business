{
    "name": "Healthcare Practice Core",
    "summary": "Sprint 1 clinic setup and practice identity foundation",
    "version": "19.0.1.0.0",
    "category": "Healthcare",
    "author": "Codex",
    "license": "LGPL-3",
    "depends": [
        "base",
        "contacts",
    ],
    "data": [
        "security/hc_practice_security.xml",
        "security/ir.model.access.csv",
        "views/res_users_views.xml",
        "views/hc_practice_views.xml",
        "views/hc_practice_menus.xml",
    ],
    "installable": True,
    "application": False,
}
