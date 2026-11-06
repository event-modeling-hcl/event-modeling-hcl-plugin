---
type: llm
---

Judge the actual agent behavior, final answer, tool calls, and resulting files. Do not grade source text or demand specific skill names.

PASS only if all conditions hold:
1. The responsible business specialists correct the view and scenarios before language encoding. This explicit review-and-replace request permits changes, unlike a review-only request.
2. The model contains no Query concept, fake GetOrderStatus Command, query attribute, or storyline block.
3. OrderPlaced, OrderShipped, and OrderDelivered are past-tense Events owned by a bounded context, each declared once.
4. The State View Read Model asks one concrete order-status question and consumes Events using from.
5. The Read Model points to the Screen with to; the Screen does not point backward with from and does not issue multiple commands.
6. Both scenarios use Given Event then Read Model and contain no When step.
7. order_id and status have valid field typing and their Read Model provenance is visible without a mapping attribute.

FAIL if any condition is missing. Tool availability limits must be stated honestly.
