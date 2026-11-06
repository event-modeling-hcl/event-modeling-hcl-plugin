---
description: Acceptance of applying feedback on a small inline input.
tags: [method, evolution]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Apply this feedback from the merge request review to the model. There is no prototype trail.

```hcl
state_change "place_order" {
  screen "checkout" {
    actor = actor.customer
    field "ship_date" { type = "date" }
    to    = [command.place_order]
  }
  command "place_order" {
    field "ship_date" { type = "date" }
    to    = [event.ordering.order_placed]
  }
}
```

Comments:
1. Sam on model/ordering.em.hcl line 3: "Label: Delivery date, not Ship date."
2. Ana on model/ordering.em.hcl line 3: "Keep Ship date, our warehouse uses that word."
3. Lee on model/ordering.em.hcl line 7: "Only one order per customer per day."
4. Kim on model/ordering.em.hcl line 1: "this is wrong"
