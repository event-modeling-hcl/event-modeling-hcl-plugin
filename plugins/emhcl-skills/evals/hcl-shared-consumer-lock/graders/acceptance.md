---
type: llm
---

Judge the actual agent behavior, final answer, tool calls, and resulting files. Do not grade source text or demand specific skill names.

PASS only if all conditions hold:
1. The agent traces field_type.orders.order_id through the canonical order_placed event into the review-status view_order read model and its scenarios, rather than inspecting only workflow-local text edits.
2. The shared field type, event, created producer, locked consumer, examples, board, and statuses remain unchanged. No partial producer edit is made while the linked consumer is locked.
3. The reply identifies view_order as locked, explains that changing the shared type indirectly changes its contract, and requests confirmation naming view_order and this UUID-to-String change before applying the chain edit.
4. Confirmation naming place_order alone does not unlock view_order. No cloned field type, alternate event, bypass workflow, status downgrade, or other workaround evades the lock.
5. No successful repair, formatting, or validation command is claimed unless it was actually executed; no production implementation code is added.

FAIL if any condition is missing. Tool availability limits must be stated honestly.
