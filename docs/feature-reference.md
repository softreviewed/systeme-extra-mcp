# Detailed feature reference


| Tool / action | What it does | When to use it | Required input |
|---|---|---|---|
| enrolments: `create` | Grant course access | Give an existing customer access after a sale | Integer `courseId`; body `contactId`, `accessType` |
| enrolments: `list` | Inspect enrolments | Audit access or identify a record before removal | None; optional string `course`, `contact` |
| enrolments: `remove` | Revoke one enrolment | Remove selected course access after authorization | String enrolment `id` |
| communities: `list` | Find communities | Identify the relevant customer community | None; optional string `query` |
| communities: `add_member` | Add an existing contact | Give a customer community access | Integer `communityId`; body integer `contactId` |
| communities: `list_members` | Inspect memberships | Audit access and find membership IDs | None; optional integer `community`, `contact` |
| communities: `remove_member` | Remove membership | Revoke selected community access | String membership `id` |
| contact_fields: `create` | Define a CRM field | Add a reusable customer-type/onboarding field | Body `fieldName`, `slug` |
| contact_fields: `update` | Rename a field label | Improve field naming without changing its slug | Parameter `slug`; body `fieldName` |
| contact_fields: `remove` | Delete a field definition | Remove an unused field after checking dependencies | Parameter `slug` |
| subscriptions: `list` | Inspect customer recurring purchases | Find subscriptions for a particular customer | Integer `contact` |
| subscriptions: `cancel` | Cancel one recurring purchase | Apply the customer's authorized cancellation timing | String subscription `id`; body `cancel` |
| webhooks: `list` | List event receivers | Audit integrations | None |
| webhooks: `get` | Inspect one receiver | Check a specific integration | String `id` |
| webhooks: `create` | Register an external receiver | Send supported events to your own service | Body `name`, `url`, `secret`, `subscriptions` |
| webhooks: `update` | Edit/pause/resume a receiver | Change events or stop delivery temporarily | String `id`; supported body fields |
| webhooks: `remove` | Delete a receiver | Remove an obsolete integration | String `id` |
| sms: `services` | Read messaging services | Check available Twilio services | None |
| sms: `numbers` | Read sender numbers | Inspect configured SMS senders | None |
| sms: `twilio_account` | Read connected account | Diagnose Twilio integration status | None |

The table uses short tool names; actual names are `systeme_extra_<name>`. Use the official connector for its existing operations, including supported contact lookup. This server does not create contacts/courses/communities, issue refunds, send SMS, host webhook receivers, manage your own paid platform plan or report affiliate earnings.

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
