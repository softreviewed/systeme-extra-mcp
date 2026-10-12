import os
import unittest
from unittest.mock import patch
import sys
from pathlib import Path
import httpx
from server import OPERATIONS, manage, prepare

sys.path.insert(0, str(Path(__file__).parent / "tests"))
from sample_inputs import inputs  # noqa: E402

# Inputs with patterns or rules that a generic generator cannot invent.
EXPLICIT_BODIES = {
    ("contact_fields", "create"): {"fieldName": "Customer", "slug": "customer"},
    ("courses", "create"): {"domainId": 1, "name": "Starter", "path": "starter-course", "themeId": 1},
    ("enrolments", "create"): {"contactId": 1, "accessType": "full_access"},
    ("pages", "apply_template"): {"templateId": "t1", "placeholders": {"headline": "Hello"}},
    ("sms", "create_template"): {"name": "Reminder", "content": "See you soon", "senderType": "PHONE_NUMBER",
                                 "phoneNumber": "+15555550100"},
    ("subscriptions", "cancel"): {"cancel": "Now"},
    ("webhooks", "create"): {"name": "Test", "secret": "hidden", "url": "https://example.com/hook",
                              "subscriptions": [{"event": "SALE_NEW", "schemaVersion": 2}]},
}


class ContractTests(unittest.TestCase):
    def test_documented_missing_twilio_responses(self):
        for action, status in (("services", 424), ("numbers", 424), ("twilio_account", 404)):
            with self.subTest(action=action), patch.dict(os.environ, {"SYSTEME_API_KEY": "test-only"}):
                result = manage("sms", action, transport=httpx.MockTransport(lambda r: httpx.Response(status)))
                self.assertIn("Twilio integration is not configured", result["error"])
                self.assertFalse(result["ok"])
    def test_every_operation_has_valid_preview(self):
        for key, entry in OPERATIONS.items():
            params, body = inputs(entry)
            body = EXPLICIT_BODIES.get(key, body)
            with self.subTest(operation=key):
                result = manage(*key, parameters=params, body=body, dry_run=True)
                self.assertTrue(result["ok"], result)

    def test_gateway_missing_secret_placeholder(self):
        with patch.dict(os.environ, {"SYSTEME_API_KEY": "<UNKNOWN>"}):
            self.assertFalse(manage("sms")["configured"])
            self.assertIn("not configured", manage("sms", "numbers")["error"])

    def test_complete_allowlist(self):
        self.assertEqual(len(OPERATIONS), 152)
        self.assertEqual(len({k[0] for k in OPERATIONS}), 22)
        for original in [("enrolments", "create"), ("communities", "add_member"), ("contact_fields", "update"),
                         ("subscriptions", "cancel"), ("webhooks", "get"), ("sms", "twilio_account")]:
            self.assertIn(original, OPERATIONS)  # v1 tool and action names stay stable

    def test_deprecated_endpoints_excluded(self):
        for entry in OPERATIONS.values():
            self.assertFalse(entry["operation"].get("deprecated"), entry["path"])

    def test_read_only_post_needs_no_confirm(self):
        def handle(request):
            return httpx.Response(200, json={"type": "object"})
        params, body = inputs(OPERATIONS[("pages", "schema")])
        with patch.dict(os.environ, {"SYSTEME_API_KEY": "test-only"}):
            result = manage("pages", "schema", params, body, transport=httpx.MockTransport(handle))
        self.assertTrue(result["ok"], result)

    def test_high_impact_write_blocked_without_confirm(self):
        result = manage("newsletters", "send", {"id": 1})
        self.assertIn("Write blocked", result["error"])
        self.assertTrue(manage("newsletters", parameters={"action": "send"})["actions"]["send"]["high_impact"])

    def test_help_is_compact_until_action_requested(self):
        summary = manage("courses")
        self.assertEqual(len(summary["actions"]), 20)
        self.assertNotIn("schemas", summary["actions"]["create"])
        detail = manage("courses", parameters={"action": "create"})
        self.assertIn("schemas", detail["actions"]["create"])
        self.assertFalse(manage("courses", parameters={"action": "nope"})["ok"])

    def test_deep_json_pointer_parameter(self):
        request = prepare("sale_settings", "payment_methods", {"currency": "usd"})
        self.assertTrue(request["path"].endswith("/usd"))

    def test_required_subscription_contact(self):
        self.assertFalse(manage("subscriptions", "list", dry_run=True)["ok"])

    def test_partial_access_modules(self):
        self.assertFalse(manage("enrolments", "create", {"courseId": 1},
                               {"contactId": 2, "accessType": "partial_access"}, dry_run=True)["ok"])

    def test_write_blocked(self):
        self.assertIn("Write blocked", manage("enrolments", "remove", {"id": "5"})["error"])

    def test_no_credential_needed_for_preview(self):
        self.assertTrue(manage("subscriptions", "cancel", {"id": "7"},
                              {"cancel": "WhenBillingPeriodEnds"}, dry_run=True)["ok"])

    def test_invalid_enum_and_unknown_fields(self):
        self.assertFalse(manage("subscriptions", "cancel", {"id": "7"}, {"cancel": "Later"}, dry_run=True)["ok"])
        self.assertFalse(manage("sms", "numbers", {"unknown": "x"}, dry_run=True)["ok"])

    def test_webhook_secret_redacted_and_schema(self):
        payload = {"name": "Test", "url": "https://example.com/events", "secret": "private",
                   "subscriptions": [{"event": "CONTACT_CREATED", "schemaVersion": 2}]}
        result = manage("webhooks", "create", body=payload, dry_run=True)
        self.assertTrue(result["ok"])
        self.assertNotIn("private", str(result))

    def test_patch_content_type(self):
        request = prepare("contact_fields", "update", {"slug": "customer_type"}, {"fieldName": "Customer type"})
        self.assertEqual(request["content_type"], "application/merge-patch+json")

    def test_path_encoding(self):
        self.assertTrue(prepare("webhooks", "get", {"id": "abc/def"})["path"].endswith("abc%2Fdef"))

    def test_mock_read_pagination_auth(self):
        def handle(request):
            self.assertEqual(request.headers["X-API-Key"], "test-only")
            self.assertEqual(request.url.params["startingAfter"], "10")
            return httpx.Response(200, json={"items": [{"id": 11}], "hasMore": True})
        with patch.dict(os.environ, {"SYSTEME_API_KEY": "test-only"}):
            result = manage("enrolments", "list", {"limit": 10, "startingAfter": 10}, transport=httpx.MockTransport(handle))
        self.assertTrue(result["data"]["hasMore"])

    def test_rate_limit_no_write_retry(self):
        calls = []
        def handle(request):
            calls.append(request)
            return httpx.Response(429, headers={"Retry-After": "5"})
        with patch.dict(os.environ, {"SYSTEME_API_KEY": "test-only"}):
            result = manage("subscriptions", "cancel", {"id": "3"}, {"cancel": "Now"}, confirm=True,
                            transport=httpx.MockTransport(handle))
        self.assertEqual(len(calls), 1)
        self.assertEqual(result["retry_after"], "5")

    def test_api_failure_is_not_empty_inventory(self):
        with patch.dict(os.environ, {"SYSTEME_API_KEY": "test-only"}):
            result = manage("webhooks", "list", transport=httpx.MockTransport(lambda r: httpx.Response(403)))
        self.assertFalse(result["ok"])
        self.assertNotIn("data", result)


if __name__ == "__main__":
    unittest.main()
