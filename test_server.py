import os
import unittest
from unittest.mock import patch
import httpx
from server import OPERATIONS, manage, prepare


class ContractTests(unittest.TestCase):
    def test_documented_missing_twilio_responses(self):
        for action, status in (("services", 424), ("numbers", 424), ("twilio_account", 404)):
            with self.subTest(action=action), patch.dict(os.environ, {"SYSTEME_API_KEY": "test-only"}):
                result = manage("sms", action, transport=httpx.MockTransport(lambda r: httpx.Response(status)))
                self.assertIn("Twilio integration is not configured", result["error"])
                self.assertFalse(result["ok"])
    def test_every_operation_has_valid_preview(self):
        bodies = {
            ("enrolments", "create"): {"contactId": 1, "accessType": "full_access"},
            ("communities", "add_member"): {"contactId": 1},
            ("contact_fields", "create"): {"fieldName": "Customer", "slug": "customer"},
            ("contact_fields", "update"): {"fieldName": "Customer type"},
            ("subscriptions", "cancel"): {"cancel": "Now"},
            ("webhooks", "create"): {"name": "Test", "secret": "hidden", "url": "https://example.com/hook",
                                      "subscriptions": [{"event": "SALE_NEW", "schemaVersion": 2}]},
            ("webhooks", "update"): {"active": False},
        }
        for key, entry in OPERATIONS.items():
            params = {p["name"]: 1 if p.get("schema", {}).get("type") == "integer" else "example"
                      for p in entry["operation"].get("parameters", []) if p.get("required")}
            with self.subTest(operation=key):
                result = manage(*key, parameters=params, body=bodies.get(key), dry_run=True)
                self.assertTrue(result["ok"], result)

    def test_gateway_missing_secret_placeholder(self):
        with patch.dict(os.environ, {"SYSTEME_API_KEY": "<UNKNOWN>"}):
            self.assertFalse(manage("sms")["configured"])
            self.assertIn("not configured", manage("sms", "numbers")["error"])

    def test_complete_allowlist(self):
        self.assertEqual(len(OPERATIONS), 20)
        self.assertEqual(len({k[0] for k in OPERATIONS}), 6)

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
