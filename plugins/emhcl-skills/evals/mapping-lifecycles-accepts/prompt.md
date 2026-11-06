---
description: Acceptance of the first two Done-when items of the mapping-lifecycles skill on a small inline domain.
tags: [method, discovery]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Stream: Subscription, identity subscriptionId.

Events: Subscription Started, Plan Upgraded, Subscription Paused, Subscription Resumed, Subscription Ended.

Commands that exist: Start Subscription, Upgrade Plan, Pause Subscription, Resume Subscription, End Subscription.

Notes: a paused subscription cannot be upgraded. An ended subscription cannot be resumed or paused.

Map the lifecycle of this stream.
