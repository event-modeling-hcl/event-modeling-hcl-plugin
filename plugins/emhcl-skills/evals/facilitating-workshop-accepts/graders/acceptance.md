---
type: llm
---

No model exists, so the first part is roles. The parts follow this order: roles, events, chapters, story order, screens, streams, lifecycles, commands, automations, external mappings, read models, command scenarios, read model scenarios, reviews, slice status, ownership, chapter summaries.

PASS if both conditions hold:
1. The session plan starts with roles, keeps the order above for each part that it covers, gives each part a time box, and has a break at least every 30 minutes because the session is remote. Parts that do not fit in 90 minutes go to a later session.
2. The plan lists the participants by role and states that each required role (product owner or domain expert, developers, tester, facilitator) is present.

FAIL if a part comes out of order (for example commands before screens, or ownership before scenarios), if a part has no time box, if 30 minutes or more pass without a break, or if the plan does not address the participants and their roles.
