---
type: llm
---

Judge command behavior and authority, not exact command names, table headings, or quotations of rules.

PASS only if all of these hold:
1. There is one collection command issued by the Collect Equipment screen for Member and one expiry command issued by the existing expiry automation for Reservation Expirer. The expiry action remains automatic; a new clerk task, member action, or approval is not an equivalent replacement.
2. Collection has typed unit and reservation identifiers from the screen and the current authenticated member and time as generated command context. Expiry has typed unit and reservation identifiers from the automation/todo input and the current time as generated command context. Earlier events of Equipment Unit supply the recorded ownership, expiry deadline, and current reservation state used by the rules. An expiry deadline carried through the todo input is also acceptable, but it cannot override the matching reservation's authoritative stream facts.
3. Both commands enforce the supplied rules against their fields and the earlier events of the Equipment Unit stream. Displayed status, displayed ownership, an Expiring Reservations row, or a refreshed read model is not made authoritative for accepting a command. Refreshing a screen for usability may be suggested but is not a substitute for checking authoritative stream facts.
4. The concrete 10:00 collection is refused because R-12 was cancelled at 09:58. It produces no Unit Collected event or new failure event. The reply does not accept it on the strength of the 09:55 Reserved display or turn this already-decided refusal into an unresolved business question.
5. Successful collection names Unit Collected and successful expiry names Reservation Expired. Expiry checks that the matching reservation is still active and the deadline has arrived; cancelled or collected reservations do not produce a Reservation Expired event.
6. The result authors commands and their records only. Existing events, screen, automation, todo list, lifecycle, and scenarios remain inputs rather than rewritten parts. A missing prerequisite may become a scoped request, not an excuse to fabricate changes in another part.

FAIL if any condition is missing. General statements about stale data, automation, or writer boundaries do not pass without the corresponding command contracts and concrete refusal.
