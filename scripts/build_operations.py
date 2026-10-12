"""Rebuild docs/operations.json from the official Systeme.io API reference.

Usage: python scripts/build_operations.py <folder of downloaded reference .md files>
Download the pages listed in https://developer.systeme.io/llms.txt first (curl works;
some Python installs reject the site's certificate chain).
"""
import json
import re
import sys
from pathlib import Path

BASE = "https://developer.systeme.io/reference/"

# "METHOD path" -> (tool group, action). Deprecated PUT endpoints are left out on purpose.
MAP = {
    "GET /api/contacts": ("contacts", "list"),
    "POST /api/contacts": ("contacts", "create"),
    "GET /api/contacts/{id}": ("contacts", "get"),
    "PATCH /api/contacts/{id}": ("contacts", "update"),
    "DELETE /api/contacts/{id}": ("contacts", "remove"),
    "POST /api/contacts/{id}/tags": ("contacts", "add_tag"),
    "DELETE /api/contacts/{id}/tags/{tagId}": ("contacts", "remove_tag"),

    "GET /api/tags": ("tags", "list"),
    "POST /api/tags": ("tags", "create"),
    "GET /api/tags/{id}": ("tags", "get"),
    "PUT /api/tags/{id}": ("tags", "update"),
    "DELETE /api/tags/{id}": ("tags", "remove"),

    "GET /api/contact_fields": ("contact_fields", "list"),
    "POST /api/contact_fields": ("contact_fields", "create"),
    "PATCH /api/contact_fields/{slug}": ("contact_fields", "update"),
    "DELETE /api/contact_fields/{slug}": ("contact_fields", "remove"),

    "GET /api/automation/rules": ("automation_rules", "list"),
    "POST /api/automation/rules": ("automation_rules", "create"),
    "GET /api/automation/rules/{id}": ("automation_rules", "get"),
    "PATCH /api/automation/rules/{id}": ("automation_rules", "update"),
    "DELETE /api/automation/rules/{id}": ("automation_rules", "remove"),

    "GET /api/booking-calendar/bookings": ("booking", "bookings"),
    "GET /api/booking-calendar/events": ("booking", "events"),
    "POST /api/booking-calendar/events": ("booking", "create_event"),
    "GET /api/booking-calendar/events/{eventId}": ("booking", "get_event"),
    "PATCH /api/booking-calendar/events/{eventId}": ("booking", "update_event"),
    "DELETE /api/booking-calendar/events/{eventId}": ("booking", "remove_event"),
    "GET /api/booking-calendar/user-availability": ("booking", "availability"),
    "POST /api/booking-calendar/user-availability": ("booking", "create_availability"),
    "PATCH /api/booking-calendar/user-availability": ("booking", "update_availability"),

    "GET /api/community/communities": ("communities", "list"),
    "POST /api/community/communities/{communityId}/memberships": ("communities", "add_member"),
    "GET /api/community/memberships": ("communities", "list_members"),
    "DELETE /api/community/memberships/{id}": ("communities", "remove_member"),

    "GET /api/domains": ("account", "domains"),
    "GET /api/files": ("account", "files"),

    "GET /api/funnels": ("funnels", "list"),
    "POST /api/funnels": ("funnels", "create"),
    "GET /api/funnels/{id}": ("funnels", "get"),
    "GET /api/funnels/{funnelId}/steps": ("funnels", "steps"),
    "POST /api/funnels/{funnelId}/steps": ("funnels", "create_step"),
    "GET /api/funnel-steps/{id}": ("funnels", "get_step"),
    "GET /api/funnels/steps": ("funnels", "search_steps"),

    "PUT /api/page-editor/pages/{id}/save": ("pages", "save"),
    "POST /api/page-editor/page-schema": ("pages", "schema"),
    "POST /api/page-editor/page-template": ("pages", "template"),
    "PUT /api/pages/{pageId}/content/from-template": ("pages", "apply_template"),

    "GET /api/mailing/newsletters": ("newsletters", "list"),
    "POST /api/mailing/newsletters": ("newsletters", "create"),
    "GET /api/mailing/newsletters/{id}": ("newsletters", "get"),
    "PATCH /api/mailing/newsletters/{id}": ("newsletters", "update"),
    "DELETE /api/mailing/newsletters/{id}": ("newsletters", "remove"),
    "GET /api/mailing/newsletters/{id}/included-tags": ("newsletters", "included_tags"),
    "PUT /api/mailing/newsletters/{id}/included-tags": ("newsletters", "set_included_tags"),
    "GET /api/mailing/newsletters/{id}/excluded-tags": ("newsletters", "excluded_tags"),
    "PUT /api/mailing/newsletters/{id}/excluded-tags": ("newsletters", "set_excluded_tags"),
    "GET /api/mailing/newsletters/{id}/schedule": ("newsletters", "schedule"),
    "PUT /api/mailing/newsletters/{id}/schedule": ("newsletters", "set_schedule"),
    "POST /api/mailing/newsletters/{id}/send": ("newsletters", "send"),
    "POST /api/mailing/newsletters/{id}/send-test": ("newsletters", "send_test"),

    "GET /api/mailing/campaigns": ("campaigns", "list"),
    "POST /api/mailing/campaigns": ("campaigns", "create"),
    "GET /api/mailing/campaigns/{id}": ("campaigns", "get"),
    "PATCH /api/mailing/campaigns/{id}": ("campaigns", "update"),
    "DELETE /api/mailing/campaigns/{id}": ("campaigns", "remove"),
    "GET /api/mailing/campaigns/{campaignId}/steps": ("campaigns", "steps"),
    "POST /api/mailing/campaigns/{campaignId}/steps": ("campaigns", "create_step"),
    "GET /api/mailing/campaign-steps/{id}": ("campaigns", "get_step"),
    "PATCH /api/mailing/campaign-steps/{id}": ("campaigns", "update_step"),
    "DELETE /api/mailing/campaign-steps/{id}": ("campaigns", "remove_step"),
    "POST /api/mailing/campaign-steps/{id}/send-test": ("campaigns", "send_test_step"),

    "GET /api/mailing/automation-emails": ("automation_emails", "list"),
    "POST /api/mailing/automation-emails": ("automation_emails", "create"),
    "GET /api/mailing/automation-emails/{id}": ("automation_emails", "get"),
    "PATCH /api/mailing/automation-emails/{id}": ("automation_emails", "update"),
    "GET /api/mailing/automation-emails-to-specific-address": ("automation_emails", "list_to_address"),
    "POST /api/mailing/automation-emails-to-specific-address": ("automation_emails", "create_to_address"),
    "GET /api/mailing/automation-emails-to-specific-address/{id}": ("automation_emails", "get_to_address"),
    "PATCH /api/mailing/automation-emails-to-specific-address/{id}": ("automation_emails", "update_to_address"),

    "GET /api/mailing/automation-emails/{id}/statistics": ("email_statistics", "automation_email"),
    "GET /api/mailing/campaign-steps/{id}/statistics": ("email_statistics", "campaign_step"),
    "GET /api/mailing/newsletters/{id}/statistics": ("email_statistics", "newsletter"),
    "GET /api/mailing/statistics/automation-emails": ("email_statistics", "automation_emails_list"),
    "GET /api/mailing/statistics/automation-emails/summary": ("email_statistics", "automation_emails_summary"),
    "GET /api/mailing/statistics/campaign-steps": ("email_statistics", "campaign_steps_list"),
    "GET /api/mailing/statistics/campaign-steps/summary": ("email_statistics", "campaign_steps_summary"),
    "GET /api/mailing/statistics/newsletters": ("email_statistics", "newsletters_list"),
    "GET /api/mailing/statistics/newsletters/summary": ("email_statistics", "newsletters_summary"),

    "GET /api/payment/coupons": ("coupons", "list"),
    "POST /api/payment/coupons": ("coupons", "create"),
    "GET /api/payment/coupons/{id}": ("coupons", "get"),
    "PATCH /api/payment/coupons/{id}": ("coupons", "update"),
    "DELETE /api/payment/coupons/{id}": ("coupons", "remove"),

    "GET /api/payment/price-plans": ("price_plans", "list"),
    "POST /api/payment/price-plans": ("price_plans", "create"),
    "GET /api/payment/price-plans/{id}": ("price_plans", "get"),
    "PATCH /api/payment/price-plans/{id}": ("price_plans", "update"),
    "DELETE /api/payment/price-plans/{id}": ("price_plans", "remove"),

    "GET /api/payment/digital-products": ("products", "list_digital"),
    "POST /api/payment/digital-products": ("products", "create_digital"),
    "GET /api/payment/digital-products/{id}": ("products", "get_digital"),
    "PATCH /api/payment/digital-products/{id}": ("products", "update_digital"),
    "DELETE /api/payment/digital-products/{id}": ("products", "remove_digital"),
    "GET /api/payment/physical-products": ("products", "list_physical"),
    "POST /api/payment/physical-products": ("products", "create_physical"),
    "GET /api/payment/physical-products/{id}": ("products", "get_physical"),
    "PATCH /api/payment/physical-products/{id}": ("products", "update_physical"),
    "DELETE /api/payment/physical-products/{id}": ("products", "remove_physical"),
    "POST /api/payment/offers": ("products", "create_offer"),
    "GET /api/payment/offers/{id}": ("products", "get_offer"),
    "PATCH /api/payment/offers/{id}": ("products", "update_offer"),

    "GET /api/payment/sale-settings/payment-methods/{currency}": ("sale_settings", "payment_methods"),
    "GET /api/payment/sale-settings/{externalId}": ("sale_settings", "get"),
    "PATCH /api/payment/sale-settings/{externalId}": ("sale_settings", "update"),

    "GET /api/payment/subscriptions": ("subscriptions", "list"),
    "POST /api/payment/subscriptions/{id}/cancel": ("subscriptions", "cancel"),

    "GET /api/school/courses": ("courses", "list"),
    "POST /api/school/courses/classic": ("courses", "create"),
    "GET /api/school/courses/{id}": ("courses", "get"),
    "PATCH /api/school/courses/{id}": ("courses", "update"),
    "DELETE /api/school/courses/{id}": ("courses", "remove"),
    "POST /api/school/courses/{id}/activate": ("courses", "activate"),
    "POST /api/school/courses/{id}/deactivate": ("courses", "deactivate"),
    "GET /api/school/course-themes": ("courses", "themes"),
    "GET /api/school/courses/{courseId}/modules-with-lectures": ("courses", "structure"),
    "GET /api/school/course-modules": ("courses", "modules"),
    "POST /api/school/courses/{courseId}/modules": ("courses", "create_module"),
    "GET /api/school/course-modules/{moduleId}": ("courses", "get_module"),
    "PATCH /api/school/course-modules/{moduleId}": ("courses", "update_module"),
    "DELETE /api/school/course-modules/{moduleId}": ("courses", "remove_module"),
    "POST /api/school/modules/{moduleId}/classic-lectures": ("courses", "create_lecture"),
    "GET /api/school/lectures/{lectureId}": ("courses", "get_lecture"),
    "PATCH /api/school/lectures/{lectureId}": ("courses", "update_lecture"),
    "DELETE /api/school/lectures/{lectureId}": ("courses", "remove_lecture"),
    "POST /api/school/lectures/{lectureId}/activate": ("courses", "activate_lecture"),
    "POST /api/school/lectures/{lectureId}/deactivate": ("courses", "deactivate_lecture"),

    "POST /api/school/courses/{courseId}/enrollments": ("enrolments", "create"),
    "GET /api/school/enrollments": ("enrolments", "list"),
    "DELETE /api/school/enrollments/{id}": ("enrolments", "remove"),

    "GET /api/sms/message-services": ("sms", "services"),
    "GET /api/sms/phone-numbers": ("sms", "numbers"),
    "GET /api/sms/twilio-account": ("sms", "twilio_account"),
    "GET /api/sms/templates": ("sms", "templates"),
    "POST /api/sms/templates": ("sms", "create_template"),
    "GET /api/sms/templates/{templateId}": ("sms", "get_template"),
    "PATCH /api/sms/templates/{templateId}": ("sms", "update_template"),
    "DELETE /api/sms/templates/{templateId}": ("sms", "remove_template"),

    "GET /api/webhooks": ("webhooks", "list"),
    "POST /api/webhooks": ("webhooks", "create"),
    "GET /api/webhooks/{id}": ("webhooks", "get"),
    "PATCH /api/webhooks/{id}": ("webhooks", "update"),
    "DELETE /api/webhooks/{id}": ("webhooks", "remove"),
}


def main(folder):
    seen, out, skipped = set(), [], []
    for page in sorted(Path(folder).glob("*.md")):
        text = page.read_text(encoding="utf-8")
        match = re.search(r"````json\n(.*?)\n````", text, re.S)
        if not match:
            raise SystemExit("No OpenAPI block in " + page.name)
        spec = json.loads(match.group(1))
        path, methods = next(iter(spec["paths"].items()))
        method, operation = next(iter(methods.items()))
        key = method.upper() + " " + path
        if operation.get("deprecated"):
            skipped.append(key)
            continue
        if key not in MAP:
            raise SystemExit("Unmapped endpoint: " + key)
        spec["info"].pop("description", None)  # same long intro on every page
        domain, action = MAP[key]
        out.append({"domain": domain, "action": action, "source": BASE + page.name, "spec": spec})
        seen.add(key)
    missing = set(MAP) - seen
    if missing:
        raise SystemExit("Mapped but not found: " + ", ".join(sorted(missing)))
    out.sort(key=lambda o: (o["domain"], o["action"]))
    target = Path(__file__).resolve().parents[1] / "docs" / "operations.json"
    target.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(out)} operations in {len({o['domain'] for o in out})} groups; skipped deprecated: {skipped}")


if __name__ == "__main__":
    main(sys.argv[1])
