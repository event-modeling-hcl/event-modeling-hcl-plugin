---
description: Audits field lineage of an inline bakery model.
tags: [method, review]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Here is our bakery model:

```hcl
board {
  workflows = [workflow.order_cake, workflow.order_list]
}

actor "customer" {
  auth_required = false
}

bounded_context "ordering" {
  aggregate "order" {}

  event "cake_ordered" {
    aggregate = aggregate.order
    field "order_id" {
      type      = "UUID"
      generated = true
    }
    field "cake" { type = "String" }
    field "price" { type = "Decimal" }
  }
}

state_change "order_cake" {
  screen "order_screen" {
    actor = actor.customer
    to    = [command.order_cake]
    field "cake" { type = "String" }
    field "pickup_date" { type = "Date" }
  }

  command "order_cake" {
    to = [event.ordering.cake_ordered]
    field "cake" { type = "String" }
    field "pickup_date" { type = "Date" }
  }
}

state_view "order_list" {
  readmodel "order_list" {
    question = "Which cakes must the kitchen bake?"
    from     = [event.ordering.cake_ordered]
    field "order_id" { type = "UUID" }
    field "cake" { type = "String" }
    field "pickup_date" { type = "Date" }
  }
}
```

Audit the whole model for fields with no origin or no consumer. Do not change anything.
