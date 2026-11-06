---
type: llm
---

Judge the proposed business model, not whether the reply uses particular phrases or repeats a method rule. Equivalent business names and evidence formats are acceptable.

PASS only if all of these hold:
1. The replacement events express at least the customer committing an order for preparation/delivery and a driver being assigned to that order. The order fact has an order identity and captures the chosen meal, quantity, delivery address, and slot; the assignment fact relates the order to its driver. A generic save, row update, or screen operation is not accepted as the business outcome.
2. Grid refresh, polling, and the success message are not retained as business events. The changing daily total is not put into an event as a captured fact. The reply explains the removal or reinterpretation of the supplied weak events rather than silently losing their useful business meaning.
3. The order facts remain traceable to SCREEN-17 and the assignment facts to OPS-6, with their supported certainty or equivalent distinction between confirmed information and unresolved information. Reframing the software labels does not discard the original source IDs or claim that an imagined paper process is new evidence.
4. Dispatch Allocator remains the actual system executor of assignment. The reply does not replace it with a clerk, dispatcher approval, or a manual allocation step. The missing no-driver behavior stays an open question, not an invented assignment, refusal, retry, or compensation rule.
5. The result stays within events and their evidence/questions/requests. It may identify a needed change in another part as a request, but it does not author replacement roles, screens, commands, automation wiring, read models, or scenarios.

FAIL if any condition is missing. Merely saying that evidence, automation, or part boundaries should be preserved does not pass if the proposed events violate them.
