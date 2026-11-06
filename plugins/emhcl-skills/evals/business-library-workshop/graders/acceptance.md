---
type: llm
---

Judge the actual agent behavior, final answer, tool calls, and resulting files. Do not grade source text or demand specific skill names.

PASS only if all conditions hold:
1. The responsible business specialists produce the workshop result without requiring HCL encoding, a .em.hcl artifact, emhcl availability, CLI gates, or a technical report header.
2. Book Borrowed and Book Returned are past-tense business facts placed in business time; the response does not start from database, service, transport, or UI component structure.
3. Borrow Book is a State Change with a member-owned checkout screen, one intent, and Book Borrowed as its successful fact. Current Loans is a separate State View answering which copies the member currently has on loan.
4. member_id and copy_id have the supplied input provenance; the response does not silently invent identifiers, return policy, loan duration, overdue rules, or implementation fields.
5. Scenarios preserve the exact already-on-loan refusal reason and produce no event for that refusal. View examples use borrowed and returned facts to explain the current-loans result, without inventing a query command.
6. No files are created or edited and no CLI commands or downloads are executed. HCL syntax is not imposed on the workshop artifact.

FAIL if any condition is missing. Tool availability limits must be stated honestly.
