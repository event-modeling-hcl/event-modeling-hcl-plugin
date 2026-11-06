---
description: Delivery estimate for six library slices.
tags: [method, delivery]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Estimate the delivery time of our library model. Do not write files. Answer in the reply.

One team, Lending, builds everything. Its velocity was 3 weighted slices per sprint in each of the last four sprints. A sprint lasts two weeks. We need one week for deployment and training outside the slices.

Slices:
| Slice | Kind | Status | Scenarios | Upstream slices (through events) |
| --- | --- | --- | --- | --- |
| Member Directory | state view | done | 2 | Register Member |
| Register Member | state change | planned | 3 | none |
| Borrow Book | state change | planned | 5 | Register Member |
| Return Book | state change | planned | 4 | Borrow Book |
| Open Loans | state view | planned | 2 | Borrow Book, Return Book |
| Charge Late Fee | automation | planned | 6, one of them a card provider failure | Return Book |
