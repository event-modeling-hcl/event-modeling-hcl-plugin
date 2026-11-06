---
description: Exercise hcl syntax only repair.
tags: [language, acceptance, migration]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill]
---

Repair only the HCL language errors in `syntax-repair.em.hcl`: the place_order command's to target must be the unquoted event.orders.order_placed traversal, and its order_id field must explicitly use field_type.orders.order_id. The business facts, workflow boundary, labels, board order, and scenario are settled; do not run a business discovery or redesign. Format and validate with compatible tooling if available.

Sandbox setup: first write the exact supplied contents below to `syntax-repair.em.hcl` in the current directory. This setup is not an approved change to the model. Then perform the request above.

```hcl
board {
  workflows = [workflow.place_order]
}

actor "customer" {
  auth_required = true
}

bounded_context "orders" {
  field_type "order_id" {
    type = "UUID"
  }

  event "order_placed" {
    fields = [field_type.order_id]
  }
}

state_change "place_order" {
  description = "The customer supplies order_id through checkout. Keep this workflow's behavior unchanged."

  screen "checkout" {
    actor  = actor.customer
    to     = [command.place_order]
    fields = [field_type.orders.order_id]
  }

  command "place_order" {
    to = ["event.orders.order_placed"]
    field "order_id" {}
  }

  scenario "order_is_placed" {
    when { command = command.place_order }
    then { event = event.orders.order_placed }
  }
}
```
