from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request


class HcIntakePublicController(http.Controller):
    _PUBLIC_FIELDS = (
        "reason_for_visit",
        "current_concerns",
        "relevant_history",
        "medications",
        "notes",
    )

    def _get_submission(self, token):
        return request.env["hc.intake.submission"].sudo().search(
            [("access_token", "=", token)],
            limit=1,
        )

    def _build_form_values(self, submission, values=None):
        source = values or {}
        if values is None:
            source = {field_name: submission[field_name] for field_name in self._PUBLIC_FIELDS}
        return {
            field_name: source.get(field_name) or ""
            for field_name in self._PUBLIC_FIELDS
        }

    def _render_form(self, submission, values=None, error_message=None):
        return request.render(
            "hc_intake.public_intake_form",
            {
                "csrf_token": request.csrf_token(),
                "error_message": error_message,
                "form_action": "/intake/%s/submit" % submission.access_token,
                "form_values": self._build_form_values(submission, values),
                "submission": submission,
            },
        )

    @http.route(
        "/intake/<string:token>",
        type="http",
        auth="public",
        methods=["GET"],
        sitemap=False,
        website=False,
    )
    def intake_form(self, token, **kwargs):
        submission = self._get_submission(token)
        if not submission:
            return request.not_found()
        if submission.status == "complete" and submission.submitted_on:
            return request.render(
                "hc_intake.public_intake_done",
                {
                    "already_submitted": True,
                    "submission": submission,
                },
            )
        return self._render_form(submission)

    @http.route(
        "/intake/<string:token>/submit",
        type="http",
        auth="public",
        methods=["POST"],
        sitemap=False,
        website=False,
    )
    def intake_submit(self, token, **post):
        submission = self._get_submission(token)
        if not submission:
            return request.not_found()
        if submission.status == "complete" and submission.submitted_on:
            return request.render(
                "hc_intake.public_intake_done",
                {
                    "already_submitted": True,
                    "submission": submission,
                },
            )
        try:
            submission.action_submit_public_intake(post)
        except ValidationError as err:
            return self._render_form(
                submission,
                values=submission._extract_public_submission_vals(post),
                error_message=err.args[0],
            )
        return request.render(
            "hc_intake.public_intake_done",
            {
                "already_submitted": False,
                "submission": submission,
            },
        )
