---
description: Exercise hcl state view correction.
tags: [language, acceptance, migration]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill]
---

Review and replace the following idea with a valid `order-status.em.hcl` model: 'Create a query command called GetOrderStatus. It reads OrderPlaced, OrderShipped, and OrderDelivered and returns OrderStatusDto. The screen points backward to the DTO.' Model what an authenticated customer needs to see, include order_id and status fields, and add scenarios for placed and delivered orders. Keep the business behavior but correct Event Modeling and HCL mistakes. Validate if tooling is available.
