---
description: Writes command scenarios for an inline kayak model.
tags: [method, scenarios]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Here is our kayak rental model:

```hcl
board {
  workflows = [workflow.rent_kayak, workflow.return_kayak, workflow.open_rentals]
}

actor "clerk" {
  auth_required = true
}

bounded_context "rental" {
  aggregate "kayak" {}

  event "kayak_rented" {
    aggregate = aggregate.kayak
    field "kayak_id" { type = "String" }
    field "renter" { type = "String" }
    field "rented_at" { type = "DateTime" }
  }

  event "kayak_returned" {
    aggregate = aggregate.kayak
    field "kayak_id" { type = "String" }
    field "returned_at" { type = "DateTime" }
    field "late_fee_euros" { type = "Decimal" }
  }
}

state_change "rent_kayak" {
  screen "rent_desk" {
    actor = actor.clerk
    to    = [command.rent_kayak]
    field "kayak_id" { type = "String" }
    field "renter" { type = "String" }
  }

  command "rent_kayak" {
    to = [event.rental.kayak_rented]
    field "kayak_id" { type = "String" }
    field "renter" { type = "String" }
    field "rented_at" {
      type      = "DateTime"
      generated = true
    }
  }

  scenario "clerk_rents_free_kayak" {
    case = "happy_path"
    when {
      command  = command.rent_kayak
      examples = [{ kayak_id = "K-7", renter = "Ana Ruiz", rented_at = "2026-06-01T09:00" }]
    }
    then {
      event    = event.rental.kayak_rented
      examples = [{ kayak_id = "K-7", renter = "Ana Ruiz", rented_at = "2026-06-01T09:00" }]
    }
  }
}

state_change "return_kayak" {
  screen "return_desk" {
    actor = actor.clerk
    to    = [command.return_kayak]
    field "kayak_id" { type = "String" }
  }

  command "return_kayak" {
    to = [event.rental.kayak_returned]
    field "kayak_id" { type = "String" }
    field "returned_at" {
      type      = "DateTime"
      generated = true
    }
  }
}

state_view "open_rentals" {
  readmodel "open_rentals" {
    question = "Which kayaks are out on the water now?"
    from     = [event.rental.kayak_rented, event.rental.kayak_returned]
    field "kayak_id" { type = "String" }
    field "renter" { type = "String" }
  }
}
```

Business rules from the rental desk handbook: a kayak that is out cannot be rented again until it is returned. A kayak that is not out cannot be returned. A rental longer than 4 hours pays a late fee of 10 euros on return.

Write the missing scenarios for the commands Rent Kayak and Return Kayak. Show them in your reply. Do not write any file.
