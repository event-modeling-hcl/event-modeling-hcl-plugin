---
description: em-validate style explanation of emhcl CI output in plain words.
tags: [language]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Our GitLab job emhcl-validate failed on a merge request of the team event model with these lines:

```
emhcl validate --profile strict model
model/12-notify-owner.em.hcl:14:5: Error EM404: Command without reason: command "notify_owner" has no incoming flow and no external_trigger.
model/90-hotspots.em.hcl:1:1: Error EM406: Open hotspot: hotspot "notification_channel" is unresolved.
```

What do these mean in plain words, and what do we have to decide or change before the MR can merge?
