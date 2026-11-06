---
type: llm
---

The model is an .em.hcl model, so the gates run in the HCL order: roles, events, streams, lifecycle states, screens, commands, and so on. Roles, events, streams, and lifecycle states pass. The first failing gate is screens, because the actors member and librarian have no screen.

PASS if both conditions hold:
1. The reply names the gates in order with pass or fail, names screens as the first failing gate and its part, and names member and librarian (or each human role) as the failing elements.
2. The reply does not work on a later part before screens. It writes or proposes no commands, read models, chapters, board order, scenarios, slice status, or owners as the next step.

FAIL if the reply names another gate as the first failing gate (for example chapters or story order), or if it starts work on a part that comes after screens.
