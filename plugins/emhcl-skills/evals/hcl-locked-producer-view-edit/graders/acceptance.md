---
type: llm
---

Judge the actual agent behavior, final answer, tool calls, and resulting files. Do not grade source text or demand specific skill names.

PASS only if all conditions hold:
1. The done workflow is not modified and its status is not changed.
2. The created state view is updated with loyalty_id typed as field_type.orders.loyalty_id and sourced through event.orders.order_placed. Existing catalog contracts need no changes and remain unchanged; no mapping DSL, linked_copy, or storyline attribute is added.
3. The reply identifies the locked screen's two commands as a bed, meaning any second command, and does not silently split that locked workflow.
4. No implementation code is generated.

FAIL if any condition is missing. Tool availability limits must be stated honestly.
