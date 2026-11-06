---
type: llm
---

Judge the actual agent behavior, final answer, tool calls, and resulting files. Do not grade source text or demand specific skill names.

PASS only if all conditions hold:
1. The supplied workshop artifact remains unchanged. No replacement model, HCL artifact, implementation code, or automatic fix is written. Review does not grant edit permission.
2. The review identifies the Registration screen's two commands as a bed, even though the commands both concern registration. It does not split or rewrite the done Register Pet slice.
3. The review flags vaccination_status as unsourced by Pet Registered and does not invent a vaccination event, default status, derivation, or business policy to fill the gap.
4. The missing Correct Owner Email result and scenarios, missing Pet Directory and Notify Owner scenarios, and undefined removal of completed notices from the pending-work list are concrete findings grounded in the supplied artifact.
5. The original notice-timing question remains unanswered and attached to Notify Owner. Findings are not presented as fabricated CLI diagnostics or EM-coded Error/Warning lines, and no machine validation is claimed.
6. The report respects done and review statuses and names what remains locked without approval for specific fixes. It does not mistake a review request for authorization to change shared contracts or locked slices.
7. No HCL skill, CLI gates, technical report header, or installation is required for this plain-English business review.

FAIL if any condition is missing. Tool availability limits must be stated honestly.
