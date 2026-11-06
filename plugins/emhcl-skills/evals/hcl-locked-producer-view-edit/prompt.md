---
description: Exercise hcl locked producer view edit.
tags: [language, acceptance, migration, permissions]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill]
---

Update `locked-order.em.hcl`. It has state_change "place_order" with status = "done" and a created state_view "view_order". Add the supplied loyalty_id field to the view only; event.orders.order_placed already supplies it as field_type.orders.loyalty_id. Do not reopen completed work. The place-order screen currently issues both place_order and apply_coupon; leave that screen locked, but say what is wrong with it.

Sandbox setup: first write the exact supplied contents below to `locked-order.em.hcl` in the current directory. This setup is not an approved change to the model. Then perform the request above.

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

  field_type "loyalty_id" {
    type = "String"
  }

  field_type "coupon_code" {
    type = "String"
  }

  event "order_placed" {
    fields = [field_type.order_id, field_type.loyalty_id]
  }

  event "coupon_applied" {
    fields = [field_type.order_id, field_type.coupon_code]
  }
}

state_change "place_order" {
  status = "done"

  screen "checkout" {
    actor  = actor.customer
    to     = [command.place_order, command.apply_coupon]
    fields = [field_type.orders.order_id, field_type.orders.loyalty_id, field_type.orders.coupon_code]
  }

  command "place_order" {
    to     = [event.orders.order_placed]
    fields = [field_type.orders.order_id, field_type.orders.loyalty_id]
  }

  command "apply_coupon" {
    to     = [event.orders.coupon_applied]
    fields = [field_type.orders.order_id, field_type.orders.coupon_code]
  }

  scenario "order_is_placed" {
    when { command = command.place_order }
    then { event = event.orders.order_placed }
  }

  scenario "coupon_is_applied" {
    when { command = command.apply_coupon }
    then { event = event.orders.coupon_applied }
  }
}

state_view "view_order" {
  status = "created"

  readmodel "order_summary" {
    question = "Which order did this customer place?"
    from     = [event.orders.order_placed]
    to       = [screen.order_summary]
    fields   = [field_type.orders.order_id]
  }

  screen "order_summary" {
    actor = actor.customer
  }

  scenario "placed_order_is_visible" {
    given { event = event.orders.order_placed }
    then { readmodel = readmodel.order_summary }
  }
}
```
