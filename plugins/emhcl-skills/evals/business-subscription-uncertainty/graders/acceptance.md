---
type: llm
---

Judge the actual agent behavior, final answer, tool calls, and resulting files. Do not grade source text or demand specific skill names.

PASS only if all conditions hold:
1. Stripe owns the external Payment Captured fact; Subscriptions owns Activate Subscription and Subscription Activated. Translation is the automation pattern across this boundary, not an external actor screen or a linked copy of the foreign fact.
2. The response keeps payment_id, subscription_id, amount, and currency with visible sources. It identifies the missing source for the required full-payment amount instead of adding an invented total or treating amount as proof of full payment.
3. The partial-payment activation question and the full-payment-amount source are attached open questions on the activation decision or its pending-work information. Neither is silently answered or marked resolved.
4. A fully paid success scenario is described conditionally on an established full-payment fact or decision, with the missing evidence made explicit; no unsupported concrete amount or partial-payment success/refusal rule is fabricated.
5. Useful known parts of the timeline and slice are produced without blocking on a broad questionnaire. The draft is not called complete or implementation-ready while its material questions are open.
6. No HCL file, CLI command, validation claim, technical report header, or implementation design is required or produced.

FAIL if any condition is missing. Tool availability limits must be stated honestly.
