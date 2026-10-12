# Detailed feature reference


All 152 actions below come from the [official Systeme.io public API reference](https://developer.systeme.io/llms.txt). Tool names are `systeme_extra_<group>`. Call `help` on any tool for the summary list, and `help` with `parameters={"action": "<name>"}` for its exact inputs and schemas.

**Type** shows whether an action changes your account. Every write needs a preview (`dry_run`), your explicit authorization and `confirm:true`. High-impact writes send email to your list, delete records, cancel a customer purchase or overwrite page content.

Two deprecated endpoints are deliberately left out (the old `PUT` versions of newsletter and coupon update); their `PATCH` replacements are included.

<!-- actions:start -->

### contacts

Contacts: list (filter by email or tags), get, create, update, remove, add_tag, remove_tag.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `add_tag` | POST | `/api/contacts/{id}/tags` | `id`, body | Write |
| `create` | POST | `/api/contacts` | body | Write |
| `get` | GET | `/api/contacts/{id}` | `id` | Read |
| `list` | GET | `/api/contacts` | None | Read |
| `remove` | DELETE | `/api/contacts/{id}` | `id` | High-impact write |
| `remove_tag` | DELETE | `/api/contacts/{id}/tags/{tagId}` | `id`, `tagId` | Write |
| `update` | PATCH | `/api/contacts/{id}` | `id`, body | Write |

### tags

Tags: list, get, create, update (rename), remove.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `create` | POST | `/api/tags` | body | Write |
| `get` | GET | `/api/tags/{id}` | `id` | Read |
| `list` | GET | `/api/tags` | None | Read |
| `remove` | DELETE | `/api/tags/{id}` | `id` | Write |
| `update` | PUT | `/api/tags/{id}` | `id`, body | Write |

### contact_fields

Custom field definitions: list, create, update, remove; not contact field values.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `create` | POST | `/api/contact_fields` | body | Write |
| `list` | GET | `/api/contact_fields` | None | Read |
| `remove` | DELETE | `/api/contact_fields/{slug}` | `slug` | Write |
| `update` | PATCH | `/api/contact_fields/{slug}` | `slug`, body | Write |

### automation_rules

Automation rules (triggers and actions): list, get, create, update, remove.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `create` | POST | `/api/automation/rules` | body | Write |
| `get` | GET | `/api/automation/rules/{id}` | `id` | Read |
| `list` | GET | `/api/automation/rules` | None | Read |
| `remove` | DELETE | `/api/automation/rules/{id}` | `id` | Write |
| `update` | PATCH | `/api/automation/rules/{id}` | `id`, body | Write |

### booking

Booking calendar: bookings, events, create/get/update/remove event, availability.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `availability` | GET | `/api/booking-calendar/user-availability` | None | Read |
| `bookings` | GET | `/api/booking-calendar/bookings` | None | Read |
| `create_availability` | POST | `/api/booking-calendar/user-availability` | body | Write |
| `create_event` | POST | `/api/booking-calendar/events` | body | Write |
| `events` | GET | `/api/booking-calendar/events` | None | Read |
| `get_event` | GET | `/api/booking-calendar/events/{eventId}` | `eventId` | Read |
| `remove_event` | DELETE | `/api/booking-calendar/events/{eventId}` | `eventId` | Write |
| `update_availability` | PATCH | `/api/booking-calendar/user-availability` | body | Write |
| `update_event` | PATCH | `/api/booking-calendar/events/{eventId}` | `eventId`, body | Write |

### communities

List communities; add_member, list_members and remove_member.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `add_member` | POST | `/api/community/communities/{communityId}/memberships` | `communityId`, body | Write |
| `list` | GET | `/api/community/communities` | None | Read |
| `list_members` | GET | `/api/community/memberships` | None | Read |
| `remove_member` | DELETE | `/api/community/memberships/{id}` | `id` | Write |

### account

Account inventory: connected domains and uploaded files (read only).

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `domains` | GET | `/api/domains` | None | Read |
| `files` | GET | `/api/files` | None | Read |

### funnels

Funnels: list, get, create, steps, create_step, get_step, search_steps.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `create` | POST | `/api/funnels` | body | Write |
| `create_step` | POST | `/api/funnels/{funnelId}/steps` | `funnelId`, body | Write |
| `get` | GET | `/api/funnels/{id}` | `id` | Read |
| `get_step` | GET | `/api/funnel-steps/{id}` | `id` | Read |
| `list` | GET | `/api/funnels` | None | Read |
| `search_steps` | GET | `/api/funnels/steps` | None | Read |
| `steps` | GET | `/api/funnels/{funnelId}/steps` | `funnelId` | Read |

### pages

Page editor: page schema and template (read), save page content, apply a template.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `apply_template` | PUT | `/api/pages/{pageId}/content/from-template` | `pageId`, body | High-impact write |
| `save` | PUT | `/api/page-editor/pages/{id}/save` | `id`, body | High-impact write |
| `schema` | POST | `/api/page-editor/page-schema` | body | Read |
| `template` | POST | `/api/page-editor/page-template` | body | Read |

### newsletters

Newsletters: list, get, create, update, remove, tag targeting, schedule, send, send_test.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `create` | POST | `/api/mailing/newsletters` | body | Write |
| `excluded_tags` | GET | `/api/mailing/newsletters/{id}/excluded-tags` | `id` | Read |
| `get` | GET | `/api/mailing/newsletters/{id}` | `id` | Read |
| `included_tags` | GET | `/api/mailing/newsletters/{id}/included-tags` | `id` | Read |
| `list` | GET | `/api/mailing/newsletters` | None | Read |
| `remove` | DELETE | `/api/mailing/newsletters/{id}` | `id` | Write |
| `schedule` | GET | `/api/mailing/newsletters/{id}/schedule` | `id` | Read |
| `send` | POST | `/api/mailing/newsletters/{id}/send` | `id` | High-impact write |
| `send_test` | POST | `/api/mailing/newsletters/{id}/send-test` | `id`, body | Write |
| `set_excluded_tags` | PUT | `/api/mailing/newsletters/{id}/excluded-tags` | `id`, body | Write |
| `set_included_tags` | PUT | `/api/mailing/newsletters/{id}/included-tags` | `id`, body | Write |
| `set_schedule` | PUT | `/api/mailing/newsletters/{id}/schedule` | `id`, body | Write |
| `update` | PATCH | `/api/mailing/newsletters/{id}` | `id`, body | Write |

### campaigns

Email campaigns and their steps: list, get, create, update, remove, steps, step changes, send_test_step.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `create` | POST | `/api/mailing/campaigns` | body | Write |
| `create_step` | POST | `/api/mailing/campaigns/{campaignId}/steps` | `campaignId`, body | Write |
| `get` | GET | `/api/mailing/campaigns/{id}` | `id` | Read |
| `get_step` | GET | `/api/mailing/campaign-steps/{id}` | `id` | Read |
| `list` | GET | `/api/mailing/campaigns` | None | Read |
| `remove` | DELETE | `/api/mailing/campaigns/{id}` | `id` | High-impact write |
| `remove_step` | DELETE | `/api/mailing/campaign-steps/{id}` | `id` | Write |
| `send_test_step` | POST | `/api/mailing/campaign-steps/{id}/send-test` | `id`, body | Write |
| `steps` | GET | `/api/mailing/campaigns/{campaignId}/steps` | `campaignId` | Read |
| `update` | PATCH | `/api/mailing/campaigns/{id}` | `id`, body | Write |
| `update_step` | PATCH | `/api/mailing/campaign-steps/{id}` | `id`, body | Write |

### automation_emails

Automation emails, including emails to a specific address: list, get, create, update.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `create` | POST | `/api/mailing/automation-emails` | body | Write |
| `create_to_address` | POST | `/api/mailing/automation-emails-to-specific-address` | body | Write |
| `get` | GET | `/api/mailing/automation-emails/{id}` | `id` | Read |
| `get_to_address` | GET | `/api/mailing/automation-emails-to-specific-address/{id}` | `id` | Read |
| `list` | GET | `/api/mailing/automation-emails` | None | Read |
| `list_to_address` | GET | `/api/mailing/automation-emails-to-specific-address` | None | Read |
| `update` | PATCH | `/api/mailing/automation-emails/{id}` | `id`, body | Write |
| `update_to_address` | PATCH | `/api/mailing/automation-emails-to-specific-address/{id}` | `id`, body | Write |

### email_statistics

[Beta] Email statistics for newsletters, campaign steps and automation emails.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `automation_email` | GET | `/api/mailing/automation-emails/{id}/statistics` | `id` | Read |
| `automation_emails_list` | GET | `/api/mailing/statistics/automation-emails` | `dateFrom`, `dateTo` | Read |
| `automation_emails_summary` | GET | `/api/mailing/statistics/automation-emails/summary` | `dateFrom`, `dateTo` | Read |
| `campaign_step` | GET | `/api/mailing/campaign-steps/{id}/statistics` | `id` | Read |
| `campaign_steps_list` | GET | `/api/mailing/statistics/campaign-steps` | `dateFrom`, `dateTo` | Read |
| `campaign_steps_summary` | GET | `/api/mailing/statistics/campaign-steps/summary` | `dateFrom`, `dateTo` | Read |
| `newsletter` | GET | `/api/mailing/newsletters/{id}/statistics` | `id` | Read |
| `newsletters_list` | GET | `/api/mailing/statistics/newsletters` | `dateFrom`, `dateTo` | Read |
| `newsletters_summary` | GET | `/api/mailing/statistics/newsletters/summary` | `dateFrom`, `dateTo` | Read |

### coupons

Coupons: list, get, create, update, remove.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `create` | POST | `/api/payment/coupons` | body | Write |
| `get` | GET | `/api/payment/coupons/{id}` | `id` | Read |
| `list` | GET | `/api/payment/coupons` | None | Read |
| `remove` | DELETE | `/api/payment/coupons/{id}` | `id` | Write |
| `update` | PATCH | `/api/payment/coupons/{id}` | `id`, body | Write |

### price_plans

Price plans: list, get, create, update, remove.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `create` | POST | `/api/payment/price-plans` | body | Write |
| `get` | GET | `/api/payment/price-plans/{id}` | `id` | Read |
| `list` | GET | `/api/payment/price-plans` | None | Read |
| `remove` | DELETE | `/api/payment/price-plans/{id}` | `id` | Write |
| `update` | PATCH | `/api/payment/price-plans/{id}` | `id`, body | Write |

### products

Digital and physical products (list, get, create, update, remove) and offers (create, get, update).

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `create_digital` | POST | `/api/payment/digital-products` | body | Write |
| `create_offer` | POST | `/api/payment/offers` | body | Write |
| `create_physical` | POST | `/api/payment/physical-products` | body | Write |
| `get_digital` | GET | `/api/payment/digital-products/{id}` | `id` | Read |
| `get_offer` | GET | `/api/payment/offers/{id}` | `id` | Read |
| `get_physical` | GET | `/api/payment/physical-products/{id}` | `id` | Read |
| `list_digital` | GET | `/api/payment/digital-products` | None | Read |
| `list_physical` | GET | `/api/payment/physical-products` | None | Read |
| `remove_digital` | DELETE | `/api/payment/digital-products/{id}` | `id` | High-impact write |
| `remove_physical` | DELETE | `/api/payment/physical-products/{id}` | `id` | High-impact write |
| `update_digital` | PATCH | `/api/payment/digital-products/{id}` | `id`, body | Write |
| `update_offer` | PATCH | `/api/payment/offers/{id}` | `id`, body | Write |
| `update_physical` | PATCH | `/api/payment/physical-products/{id}` | `id`, body | Write |

### sale_settings

Sale settings: available payment methods per currency; get and update by external id.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `get` | GET | `/api/payment/sale-settings/{externalId}` | `externalId` | Read |
| `payment_methods` | GET | `/api/payment/sale-settings/payment-methods/{currency}` | `currency` | Read |
| `update` | PATCH | `/api/payment/sale-settings/{externalId}` | `externalId`, body | Write |

### subscriptions

List customer subscriptions (contact required) or cancel using Now / WhenBillingPeriodEnds. Not the owner's platform plan.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `cancel` | POST | `/api/payment/subscriptions/{id}/cancel` | `id`, body | High-impact write |
| `list` | GET | `/api/payment/subscriptions` | `contact` | Read |

### courses

Courses, modules and lectures: list, get, create, update, remove, activate, deactivate, themes, structure.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `activate` | POST | `/api/school/courses/{id}/activate` | `id` | Write |
| `activate_lecture` | POST | `/api/school/lectures/{lectureId}/activate` | `lectureId` | Write |
| `create` | POST | `/api/school/courses/classic` | body | Write |
| `create_lecture` | POST | `/api/school/modules/{moduleId}/classic-lectures` | `moduleId`, body | Write |
| `create_module` | POST | `/api/school/courses/{courseId}/modules` | `courseId`, body | Write |
| `deactivate` | POST | `/api/school/courses/{id}/deactivate` | `id` | Write |
| `deactivate_lecture` | POST | `/api/school/lectures/{lectureId}/deactivate` | `lectureId` | Write |
| `get` | GET | `/api/school/courses/{id}` | `id` | Read |
| `get_lecture` | GET | `/api/school/lectures/{lectureId}` | `lectureId` | Read |
| `get_module` | GET | `/api/school/course-modules/{moduleId}` | `moduleId` | Read |
| `list` | GET | `/api/school/courses` | None | Read |
| `modules` | GET | `/api/school/course-modules` | None | Read |
| `remove` | DELETE | `/api/school/courses/{id}` | `id` | High-impact write |
| `remove_lecture` | DELETE | `/api/school/lectures/{lectureId}` | `lectureId` | Write |
| `remove_module` | DELETE | `/api/school/course-modules/{moduleId}` | `moduleId` | Write |
| `structure` | GET | `/api/school/courses/{courseId}/modules-with-lectures` | `courseId` | Read |
| `themes` | GET | `/api/school/course-themes` | None | Read |
| `update` | PATCH | `/api/school/courses/{id}` | `id`, body | Write |
| `update_lecture` | PATCH | `/api/school/lectures/{lectureId}` | `lectureId`, body | Write |
| `update_module` | PATCH | `/api/school/course-modules/{moduleId}` | `moduleId`, body | Write |

### enrolments

Manage student enrolments: create, list, remove. Supports full, partial and drip course access.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `create` | POST | `/api/school/courses/{courseId}/enrollments` | `courseId`, body | Write |
| `list` | GET | `/api/school/enrollments` | None | Read |
| `remove` | DELETE | `/api/school/enrollments/{id}` | `id` | Write |

### sms

SMS: Twilio configuration reads (services, numbers, twilio_account) and SMS template management. Does not send SMS.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `create_template` | POST | `/api/sms/templates` | body | Write |
| `get_template` | GET | `/api/sms/templates/{templateId}` | `templateId` | Read |
| `numbers` | GET | `/api/sms/phone-numbers` | None | Read |
| `remove_template` | DELETE | `/api/sms/templates/{templateId}` | `templateId` | Write |
| `services` | GET | `/api/sms/message-services` | None | Read |
| `templates` | GET | `/api/sms/templates` | None | Read |
| `twilio_account` | GET | `/api/sms/twilio-account` | None | Read |
| `update_template` | PATCH | `/api/sms/templates/{templateId}` | `templateId`, body | Write |

### webhooks

List, get, create, update, remove webhook configurations. This does not run an event listener. Secrets are redacted.

| Action | Method | Path | Required input | Type |
|---|---|---|---|---|
| `create` | POST | `/api/webhooks` | body | Write |
| `get` | GET | `/api/webhooks/{id}` | `id` | Read |
| `list` | GET | `/api/webhooks` | None | Read |
| `remove` | DELETE | `/api/webhooks/{id}` | `id` | Write |
| `update` | PATCH | `/api/webhooks/{id}` | `id`, body | Write |

<!-- actions:end -->

## Rules and limits

### Course access rules

`accessType`: `full_access`, `partial_access`, `dripping_content`, `partial_dripping_access`. Partial access requires a non-empty integer `modules` array. These tools select enrolment access type; they do not configure lesson schedules. Revoking access is not a refund.

### Contact fields and subscriptions

Field actions manage **definitions, not individual contact values**. Names are limited to 255 characters; slugs such as `customer_type` must match the documented word-character pattern. Update changes the label, not the slug. Review dependent forms/workflows before removal.

Customer subscriptions are **customers' recurring purchases**, not your own Systeme.io subscription. Listing needs a real contact ID and may return an empty collection. Cancellation uses exactly `Now` or `WhenBillingPeriodEnds`; it does not refund payments.

### Webhook and SMS limits

Supported webhook events: `CONTACT_CREATED`, `CONTACT_TAG_ADDED`, `CONTACT_TAG_REMOVED`, `CONTACT_OPT_IN`, `SALE_NEW`, `SALE_CANCELED`. Prefer objects such as `{"event":"SALE_NEW","schemaVersion":2}`; the checked schema deprecates legacy string-array subscriptions.

Webhook update accepts `name`, `secret`, `subscriptions`, `active`; **changing `url` is not supported by the checked update schema**. Setting `active:false` pauses delivery. Your external service must receive/process events; authorize the destination before forwarding customer data.

SMS tools inspect configuration only. Connect Twilio in Systeme.io first. The documented missing-integration responses are 424 for services/numbers and 404 for the account. They do not establish that a paid Systeme.io plan is required. [Official Twilio setup](https://help.systeme.io/article/4477-how-to-integrate-your-twilio-account-with-systemeio).


[Back to README](../README.md)
