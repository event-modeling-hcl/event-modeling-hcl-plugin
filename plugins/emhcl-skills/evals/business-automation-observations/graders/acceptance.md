---
type: llm
---

Judge the actual agent behavior, final answer, tool calls, and resulting files. Do not grade source text or demand specific skill names.

PASS only if all conditions hold:
1. All four supplied cases remain visible: row enters, command is dispatched and produces its event, completion removes the row, and an empty-list recheck dispatches nothing.
2. Order Placed is the opening fact and Order Confirmation Requested is the closing fact for the internal worker's pending list; the response does not replace the list with an unexplained status flag or invisible trigger.
3. O-17 and its order_id provenance remain consistent through the supplied facts, pending row, issued command, and command result.
4. The response can separate dispatch and command-result scenarios, but does not drop the dispatch observation because a technical HCL action scenario asserts an event instead of a Then-command.
5. No-command-dispatched remains an observable absence of dispatch. It is not rewritten as a refusal, a failure event, an invented error string, an idempotency policy, or a successful no-op command.
6. Workshop Given/When/Then prose is accepted without requiring typed HCL targets, HCL scenario grammar, the HCL skill, or CLI execution.

FAIL if any condition is missing. Tool availability limits must be stated honestly.
