---
description: Exercise hcl external translation.
tags: [language, acceptance, migration]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill]
---

From this requirement, create `payment-activation.em.hcl`: Stripe sends Payment Captured. Our Subscriptions domain uses that fact to Activate Subscription and records Subscription Activated. The payment message contains payment_id, subscription_id, amount, and currency. We do not yet know whether partial payments activate a subscription. Model that uncertainty rather than choosing a rule. Include a success scenario and validate the model if possible.
