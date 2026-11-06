# Worked example: ownership in a bike rental

A city runs a bike rental. Three teams build it: Rental, Billing, and Fleet. A card provider charges the rider.

## System boundaries

Rental system
- Owner team: Rental.
- Responsibilities: start and end a ride.
- Commands: Start Ride, End Ride.
- Events produced: Ride Started, Ride Ended, Bike Taken Out Of Service.
- Events used: Bike Blocked from Fleet, through a translation step.
- Read models: Active Rides, Ride History.
- Stream identity: one ride.

Billing system
- Owner team: Billing.
- Responsibilities: charge each ride.
- Commands: Recognize Ride Completion, Charge Ride, Send Receipt.
- Events produced: Ride Completed, Ride Charged, Charge Declined, Receipt Sent.
- Events used: Ride Ended from Rental, translated to Billing's Ride Completed before the charging decision.
- Read models: Rental Rides To Translate, Rides To Charge, Rider Invoices.
- Dependencies: the card provider.
- Stream identity: one charge.

Fleet system
- Owner team: Fleet.
- Responsibilities: keep bikes ready.
- Commands: Report Damage, Block Bike.
- Events produced: Damage Reported, Bike Blocked.
- Read models: Bikes To Repair.
- Stream identity: one bike.

## Event flow across boundaries

1. Rental writes Ride Started.
2. Rental writes Ride Ended. Billing translates it through Recognize Ride Completion into its own Ride Completed fact.
3. Billing's worker decides the charge from Ride Completed and writes Ride Charged or Charge Declined.
4. Fleet writes Bike Blocked. The work moves to Rental, which writes Bike Taken Out Of Service and refuses new rides on that bike.

## Team responsibility matrix

| Team | Commands | Events | Read models |
| --- | --- | --- | --- |
| Rental | Start Ride, End Ride | Ride Started, Ride Ended, Bike Taken Out Of Service | Active Rides, Ride History |
| Billing | Recognize Ride Completion, Charge Ride, Send Receipt | Ride Completed, Ride Charged, Charge Declined, Receipt Sent | Rental Rides To Translate, Rides To Charge, Rider Invoices |
| Fleet | Report Damage, Block Bike | Damage Reported, Bike Blocked | Bikes To Repair |

## Communication between teams

Rental to Billing
- Trigger: Ride Ended.
- Reaction: Billing translates Ride Ended into its local Ride Completed. Its Ride Charger then reads Rides To Charge and issues Charge Ride.
- Result: Ride Completed, then Ride Charged or Charge Declined.

Fleet to Rental
- Trigger: Bike Blocked.
- Reaction: a translation step of Rental issues Take Bike Out Of Service.
- Result: Bike Taken Out Of Service. Start Ride then refuses that bike.

## Automations

Ride Charger
- Starts on: Billing's Ride Completed, through Rides To Charge. The earlier Rental fact passes through translation first.
- Decides: the amount from the duration and the tariff.
- Issues: Charge Ride.
- Home team: Billing, because Billing owns Charge Ride.

Receipt Mailer
- Starts on: Ride Charged.
- Decides: nothing. It informs the rider.
- Issues: Send Receipt, which records Receipt Sent.
- Home team: Billing, because Billing owns Send Receipt.

## External systems

| System | Owner team | Talks to | Purpose |
| --- | --- | --- | --- |
| Card provider | Billing | Billing system | Charge the card |

## Independent work

Each team owns its events and read models and deploys alone. Teams agree only on the events that cross a boundary: Ride Ended and Bike Blocked. No cycle exists: Fleet feeds Rental, and Rental feeds Billing.

## In an .em.hcl model

The owner of an event is the owner of its context. Each workflow carries its own owner. The teams and the external system come from the roles part.

The contexts below belong to one modeled system but different teams. The translation remains a business boundary even when a tool calls it an internal worker. The example shows completed elements supplied by their respective writers.

```hcl
team "rental_team" {}

team "billing_team" {}

system "card_provider" {
  external = true
}

bounded_context "rental" {
  owner = team.rental_team

  event "ride_ended" {
    field "ride_id" {
      type = "UUID"
    }
  }
}

bounded_context "billing" {
  owner = team.billing_team

  event "ride_completed" {
    field "ride_id" {
      type = "UUID"
    }
  }

  event "ride_charged" {
    field "ride_id" {
      type = "UUID"
    }
  }
}

state_change "end_ride" {
  owner = team.rental_team

  screen "end_ride_button" {
    actor = actor.rider
    to    = [command.end_ride]
  }

  command "end_ride" {
    to = [event.rental.ride_ended]
  }
}

automation "recognize_ride_completion" {
  owner       = team.billing_team
  description = "Translate Rental's Ride Ended into Billing's Ride Completed before the charging decision."

  readmodel "rental_rides_to_translate" {
    question = "Which completed rides does Rental report?"
    from     = [event.rental.ride_ended]
    to       = [processor.ride_completion_translator]
  }

  processor "ride_completion_translator" {
    to = [command.recognize_ride_completion]
  }

  command "recognize_ride_completion" {
    to = [event.billing.ride_completed]
  }
}

hotspot "internal_translation_boundary" {
  question = "The tool classifies this internal cross-team translation as a worker. How will the translation contract stay visible?"
  on       = workflow.recognize_ride_completion
}

automation "charge_ended_ride" {
  owner = team.billing_team

  readmodel "rides_to_charge" {
    question = "Which ended rides are not charged yet?"
    from     = [event.billing.ride_completed, event.billing.ride_charged]
    to       = [processor.ride_charger]
  }

  processor "ride_charger" {
    to = [command.charge_ride]
  }

  command "charge_ride" {
    to = [event.billing.ride_charged]
  }
}
```

HCL v0.8.0 has no request `concerns` value for a team. If the Fleet team is missing, record a question instead. Do not label a team as an actor to route the request.

```hcl
hotspot "fleet_team_missing" {
  kind     = "question"
  category = "who"
  question = "Which team owns the bikes, and must the model declare Fleet?"
}
```
