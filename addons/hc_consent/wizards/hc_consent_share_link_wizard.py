from odoo import fields, models


class HcConsentShareLinkWizard(models.TransientModel):
    _name = "hc.consent.share.link.wizard"
    _description = "Healthcare Consent Share Link"

    consent_record_id = fields.Many2one(
        "hc.consent.record",
        string="Consent Record",
        required=True,
        readonly=True,
    )
    share_url = fields.Char(string="Shareable Link", required=True, readonly=True)

    def action_open_link(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": self.share_url,
            "target": "new",
        }
