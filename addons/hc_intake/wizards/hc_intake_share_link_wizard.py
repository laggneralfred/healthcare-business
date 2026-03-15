from odoo import fields, models


class HcIntakeShareLinkWizard(models.TransientModel):
    _name = "hc.intake.share.link.wizard"
    _description = "Healthcare Intake Share Link"

    intake_submission_id = fields.Many2one(
        "hc.intake.submission",
        string="Intake Record",
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
