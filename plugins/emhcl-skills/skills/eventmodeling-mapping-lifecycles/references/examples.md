# Lifecycle example: a hotel booking

Use this example to see states, moves, refused moves, and alternative paths of one stream.

## Moves

| From state | Command | Events | To state | Valid |
| --- | --- | --- | --- | --- |
| (none) | Open booking | Booking opened | Draft | yes |
| Draft | Confirm booking | Booking confirmed | Booked | yes |
| Draft | Cancel booking | Booking canceled | Canceled | yes |
| Booked | Cancel booking | Booking canceled | Canceled | yes |
| Booked | Start stay | Stay started | Staying | yes |
| Staying | End stay | Stay ended | Closed | yes |
| Booked | Return to draft | none | Booked | no: a confirmed booking cannot go back |
| Canceled | Confirm booking | none | Canceled | no: a canceled booking cannot be confirmed |
| Draft | Start stay | none | Draft | no: a stay cannot start before the booking is confirmed |

## States

| State | End | Path |
| --- | --- | --- |
| Draft | no | main |
| Booked | no | main |
| Staying | no | main |
| Closed | yes | main |
| Canceled | yes | cancel |

## Walk of the paths

- Main: Draft, Booked, Staying, Closed. No event is missing.
- Cancel: from Draft or Booked to Canceled. It ends.
- Failure: the person says that a payment failure at confirmation leaves the booking in Draft. The command is refused. No event exists, so this is a refused move and no failure state.

## In an .em.hcl model

Step 1, before the commands exist: write the states only. The lifecycles gate stays open.

```hcl
lifecycle "booking" {
  aggregate = aggregate.booking.booking

  state "draft" {
    path = "main"
  }

  state "booked" {
    path = "main"
  }

  state "canceled" {
    end  = true
    path = "cancel"
  }
}
```

Step 2, after the command `confirm_booking` exists: add its move and its refused move inside the same lifecycle.

```hcl
  transition "confirm_booking" {
    command = command.confirm_booking.confirm_booking
    events  = [event.booking.booking_confirmed]
    before  = [state.draft]
    after   = state.booked
  }

  invalid_transition "confirm_canceled_booking" {
    command = command.confirm_booking.confirm_booking
    before  = [state.canceled]
    reason  = "A canceled booking cannot be confirmed."
  }
```
