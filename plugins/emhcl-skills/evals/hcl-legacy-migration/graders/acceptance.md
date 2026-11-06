---
type: llm
---

Judge the actual agent behavior, final answer, tool calls, and resulting files. Do not grade source text or demand specific skill names.

PASS only if all conditions hold:
1. When a compatible CLI is available, the agent uses `emhcl migrate -w legacy.em.hcl` and reads its report rather than hand-converting v0.4.0 constructs. A non-writing preview is allowed but not required. Without the CLI, the limitation is explicit and no executed migration or validation is claimed.
2. The result has one board listing place_order, view_order, and import_partner_order in their former order, explicit qualified field_type.orders.order_id or field_type.partner.partner_order_id types on every formerly typeless field, and automation in place of translation.
3. Customer purchases and Checkout purchase remain as meaningful titles. Migration-generated titles that merely repeat an ID's words, such as Order Placed, View Order, and Import Partner Order, are removed; no blanket keep-all or delete-all title policy is used.
4. The migrated model is formatted and validated with emhcl validate legacy.em.hcl when compatible tooling is available, and the observed migration report and command results are reported.

FAIL if any condition is missing. Tool availability limits must be stated honestly.
