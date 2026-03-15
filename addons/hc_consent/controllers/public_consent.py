from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request


class HcConsentPublicController(http.Controller):
    _PUBLIC_FIELDS = (
        "consent_given_by",
        "consent_summary",
        "notes",
    )

    def _get_record(self, token):
        return request.env["hc.consent.record"].sudo().search(
            [("access_token", "=", token)],
            limit=1,
        )

    def _build_form_values(self, record, values=None):
        source = values or {}
        if values is None:
            source = {field_name: record[field_name] for field_name in self._PUBLIC_FIELDS}
        return {
            field_name: source.get(field_name) or ""
            for field_name in self._PUBLIC_FIELDS
        }

    def _render_form(self, record, values=None, error_message=None):
        return request.render(
            "hc_consent.public_consent_form",
            {
                "csrf_token": request.csrf_token(),
                "error_message": error_message,
                "form_action": "/consent/%s/submit" % record.access_token,
                "form_values": self._build_form_values(record, values),
                "record": record,
            },
        )

    @http.route(
        "/consent/<string:token>",
        type="http",
        auth="public",
        methods=["GET"],
        sitemap=False,
        website=False,
    )
    def consent_form(self, token, **kwargs):
        record = self._get_record(token)
        if not record:
            return request.not_found()
        if record.status == "complete" and record.signed_on:
            return request.render(
                "hc_consent.public_consent_done",
                {
                    "already_submitted": True,
                    "record": record,
                },
            )
        return self._render_form(record)

    @http.route(
        "/consent/<string:token>/submit",
        type="http",
        auth="public",
        methods=["POST"],
        sitemap=False,
        website=False,
    )
    def consent_submit(self, token, **post):
        record = self._get_record(token)
        if not record:
            return request.not_found()
        if record.status == "complete" and record.signed_on:
            return request.render(
                "hc_consent.public_consent_done",
                {
                    "already_submitted": True,
                    "record": record,
                },
            )
        try:
            record.action_submit_public_consent(post)
        except ValidationError as err:
            return self._render_form(
                record,
                values=record._extract_public_consent_vals(post),
                error_message=err.args[0],
            )
        return request.render(
            "hc_consent.public_consent_done",
            {
                "already_submitted": False,
                "record": record,
            },
        )
