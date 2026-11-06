---
type: llm
---

Judge the actual agent behavior, final answer, tool calls, and resulting files. Do not grade source text or demand specific skill names.

PASS only if all conditions hold:
1. The responsible business specialists establish the timeline, commands, views, automation, and scenarios before language encoding. Language syntax is not a substitute for business discovery.
2. The output is a `.em.hcl` file with lower-snake-case block labels, context-owned Events, one `board` block that lists every workflow in business-time order, and an explicit `type` on every field and subfield.
3. Borrowing is a state_change with Screen to Command and Command to Event expressed in canonical direction.
4. Current loans is a state_view whose Read Model has a concrete question and whose scenario has Given Event and Then Read Model with no When step.
5. The overdue notice reaction is an automation consuming only internal Events, with a pending-work read model feeding the processor, and includes a machine-action scenario using HCL When/Then grammar.
6. member_id and copy_id are reusable UUID field types and connected contract fields pass an information-provenance review without a mapping DSL.
7. The already-on-loan rule appears as an observable error scenario rather than invented implementation logic or expect_empty_list.

FAIL if any condition is missing. Tool availability limits must be stated honestly.
