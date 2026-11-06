---
description: Exercise hcl legacy migration.
tags: [language, acceptance, migration]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill]
---

The supplied `legacy.em.hcl` is a v0.4.0 model: it has no board, typeless order_id and partner_order_id fields backed by uniquely named field types, and translation "import_partner_order". Bring it to the current language without changing its meaning and validate it if the CLI is available. Preserve meaningful existing titles such as Customer purchases and Checkout purchase; do not leave redundant titles that merely spell out an ID.

Sandbox setup: first write the exact supplied contents below to `legacy.em.hcl` in the current directory. This setup is not an approved change to the model. Then perform the request above.

```hcl
bounded_context "orders" {
  title = "Customer purchases"

  field_type "order_id" {
    type = "UUID"
  }

  event "order_placed" {
    field "order_id" {}
  }
}

system "partner" {
  external = true
}

bounded_context "partner" {
  owner    = system.partner
  external = true

  field_type "partner_order_id" {
    type = "UUID"
  }

  event "partner_order_shared" {
    field "partner_order_id" {}
  }
}

actor "customer" {
  auth_required = true
}

state_change "place_order" {
  title = "Checkout purchase"

  screen "checkout" {
    actor = actor.customer
    to    = [command.place_order]
    field "order_id" {}
  }

  command "place_order" {
    to = [event.orders.order_placed]
    field "order_id" {}
  }

  scenario "order_is_placed" {
    when { command = command.place_order }
    then { event = event.orders.order_placed }
  }
}

state_view "view_order" {
  readmodel "order_summary" {
    question = "Which order was placed?"
    from     = [event.orders.order_placed]
    to       = [screen.order_summary]
    field "order_id" {}
  }

  screen "order_summary" {
    actor = actor.customer
  }

  scenario "placed_order_is_visible" {
    given { event = event.orders.order_placed }
    then { readmodel = readmodel.order_summary }
  }
}

translation "import_partner_order" {
  description = "The partner order identifier is the receiving domain's order identifier; this is a rename, not a newly generated value."

  processor "order_importer" {
    from = [event.partner.partner_order_shared]
    to   = [command.import_order]
    field "partner_order_id" {}
  }

  command "import_order" {
    description = "Rename partner_order_id from the incoming partner fact to order_id."
    to          = [event.orders.order_placed]
    field "order_id" {}
  }

  scenario "partner_order_is_imported" {
    given { event = event.partner.partner_order_shared }
    when { processor = processor.order_importer }
    then { event = event.orders.order_placed }
  }
}
```
