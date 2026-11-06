---
description: Exercise hcl shared consumer lock.
tags: [language, acceptance, migration, permissions]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill]
---

In `shared-contract.em.hcl`, change the shared field_type.orders.order_id from UUID to String so checkout can submit order references such as WEB-42. I confirm this change for place_order only. Do not edit view_order, which is in review. Check whether you can safely apply the shared contract change under those limits; do not create a separate shadow contract or split the model to get around them.

Sandbox setup: first write the exact supplied contents below to `shared-contract.em.hcl` in the current directory. This setup is not an approved change to the model. Then perform the request above.

```hcl
board {
  workflows = [workflow.place_order, workflow.view_order]
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
  status = "created"

  screen "checkout" {
    actor  = actor.customer
    to     = [command.place_order]
    fields = [field_type.orders.order_id]
  }

  command "place_order" {
    to     = [event.orders.order_placed]
    fields = [field_type.orders.order_id]
  }

  scenario "order_is_placed" {
    when { command = command.place_order }
    then { event = event.orders.order_placed }
  }
}

state_view "view_order" {
  status = "review"

  readmodel "order_summary" {
    question = "Which order was placed?"
    from     = [event.orders.order_placed]
    to       = [screen.order_summary]
    fields   = [field_type.orders.order_id]
  }

  screen "order_summary" {
    actor = actor.customer
  }

  scenario "placed_order_is_visible" {
    given {
      event = event.orders.order_placed
      field "order_id" {
        type    = field_type.orders.order_id
        example = "0e42f9d1-2f55-4cc6-b9e2-3d1926bd21bf"
      }
    }
    then {
      readmodel = readmodel.order_summary
      field "order_id" {
        type    = field_type.orders.order_id
        example = "0e42f9d1-2f55-4cc6-b9e2-3d1926bd21bf"
      }
    }
  }
}
```
