---
type: llm
---

PASS if the reply derives exactly one command for the Book action, one for the Confirm action, and one for the 10-minute lapse trigger (issued by an automation or the Hold Expirer, not by a screen), AND each command names exactly one issuer and one specific role or system actor (Member or Hold Expirer, never a generic user). FAIL if any action or the lapse trigger lacks a command, if a command has two issuers, or if a command names a generic user.
