---
description: Plain questions with evidence and no model words, on a small inline model.
tags: [method, review]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Here is our bike rental model. Read it as a fresh business analyst and give me the questions for the product owner about what is unclear or missing. Do not stop to ask me anything. Reply with the questions and the records you would add, do not edit files.

```hcl
board {
  workflows = [workflow.start_rental, workflow.active_rentals, workflow.return_bike]
}

actor "rider" {
  auth_required = true
}

bounded_context "rental" {
  aggregate "rental" {}

  field_type "rental_id" {
    type = "UUID"
  }

  field_type "bike_number" {
    type = "String"
  }

  field_type "rider_phone" {
    type = "String"
    pii  = true
  }

  event "rental_started" {
    aggregate = aggregate.rental
    fields    = [field_type.rental_id, field_type.bike_number, field_type.rider_phone]
  }

  event "bike_returned" {
    aggregate = aggregate.rental
    fields    = [field_type.rental_id, field_type.bike_number]
  }
}

chapter "renting" {
  workflows = [workflow.start_rental, workflow.active_rentals, workflow.return_bike]
}

state_change "start_rental" {
  screen "start_rental" {
    actor  = actor.rider
    to     = [command.start_rental]
    fields = [field_type.rental.bike_number, field_type.rental.rider_phone]
  }

  command "start_rental" {
    aggregate = aggregate.rental.rental
    to        = [event.rental.rental_started]
    fields    = [field_type.rental.bike_number, field_type.rental.rider_phone]
  }

  scenario "rider_starts_a_rental" {
    case = "happy_path"
    when { command = command.start_rental }
    then { event = event.rental.rental_started }
  }

  scenario "rider_with_three_open_rentals_is_refused" {
    case = "limit"
    given { event = event.rental.rental_started }
    given { event = event.rental.rental_started }
    given { event = event.rental.rental_started }
    when { command = command.start_rental }
    then { error = "A rider can hold at most 3 open rentals." }
  }
}

state_view "active_rentals" {
  readmodel "active_rentals" {
    question = "Which bikes are out on rental right now?"
    from     = [event.rental.rental_started, event.rental.bike_returned]
    to       = [screen.active_rentals]
    fields   = [field_type.rental.rental_id, field_type.rental.bike_number]
  }

  screen "active_rentals" {
    actor = actor.rider
  }

  scenario "started_rental_appears" {
    case = "appear"
    given { event = event.rental.rental_started }
    then { readmodel = readmodel.active_rentals }
  }
}

state_change "return_bike" {
  screen "return_bike" {
    actor  = actor.rider
    to     = [command.return_bike]
    fields = [field_type.rental.rental_id, field_type.rental.bike_number]
  }

  command "return_bike" {
    aggregate = aggregate.rental.rental
    to        = [event.rental.bike_returned]
    fields    = [field_type.rental.rental_id, field_type.rental.bike_number]
  }

  scenario "rider_returns_bike" {
    case = "happy_path"
    given { event = event.rental.rental_started }
    when { command = command.return_bike }
    then { event = event.rental.bike_returned }
  }
}
```
