---
type: llm
---

PASS if the lifecycle has exactly one start move (Start Subscription with Subscription Started, from no state) and at least one end state (for example Ended), and each refused move names the states, the command, and a business reason, at least: Upgrade Plan refused in Paused, and Resume Subscription and Pause Subscription refused in Ended. FAIL if there is no start move or more than one, if no end state is marked, or if a refused move lacks its state or its reason.
