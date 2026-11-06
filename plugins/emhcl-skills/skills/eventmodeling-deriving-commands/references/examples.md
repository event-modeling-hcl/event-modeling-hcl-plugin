# Worked command examples

The values are new and only show the idea.

## A screen command: Reserve Bike

The screen "Pick a Bike" offers the action "Reserve". It becomes the command "Reserve Bike".

| Part | Value |
| --- | --- |
| Issuer | Pick a Bike |
| Role | Rider |
| Fields | bike number (text, from the screen), start time (date and time, from the screen), rider number (text, generated: acting user), requested at (date and time, generated: current time) |
| Rule | The start time is after the requested at time. |
| Precondition | The bike stream is in the state "Available". |
| Success | Bike Reserved, with reserved at taken from requested at |
| Failures | Start time in the past (rejection), bike not available (rejection) |

The rule reads the start time and the requested at time. Both are command fields. The precondition reads the bike state from earlier events. No value comes from a clock or a session at decision time.

## A trigger inside the system: Expire Reservation

A reservation holds for 15 minutes. A timer inside the system fires when that time ends. The timer is a trigger inside the system, so it becomes the command "Expire Reservation", issued by an automation.

| Part | Value |
| --- | --- |
| Issuer | Reservation Expirer (automation) |
| Role | Reservation Expirer |
| Fields | reservation number (text, from the todo list), expired at (date and time, generated: current time) |
| Precondition | The reservation stream is in the state "Reserved". |
| Success | Reservation Expired |
| Failures | Ride already started (rejection) |

A payment provider that reports a cleared payment is different. That report is an event from another system. Derive no command for it. Write a request on the event, concerning automations.

## A conditional field: Pay Order

| Field | Condition |
| --- | --- |
| payment method | always |
| card number, expiry month | only when payment method is card |
| bank account | only when payment method is transfer |

## In an .em.hcl model

```hcl
state_change "reserve_bike" {
  screen "pick_a_bike" {
    actor = actor.rider
    to    = [command.reserve_bike]
  }

  command "reserve_bike" {
    to = [event.rental.bike_reserved]

    field "bike_number" {
      type = "String"
    }

    field "requested_at" {
      type      = "DateTime"
      generated = true
    }
  }
}
```
