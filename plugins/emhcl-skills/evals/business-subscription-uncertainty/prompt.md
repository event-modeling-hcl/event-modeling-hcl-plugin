---
description: Exercise business subscription uncertainty.
tags: [business, acceptance, migration]
max_turns: 25
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Make a business-only workshop draft, in your reply, for subscription activation. Stripe reports Payment Captured with payment_id, subscription_id, amount, and currency. The Subscriptions domain translates that external fact into its own language: Activate Subscription records Subscription Activated. A fully paid subscription activates. We have not decided whether a partial payment activates it, and we do not know where the required full-payment amount comes from. Continue useful modeling without making those decisions for us. No HCL or CLI work.
