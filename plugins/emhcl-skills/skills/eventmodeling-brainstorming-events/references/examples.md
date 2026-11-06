# Brainstorming example: a city bike rental

Use this example to see how a first list becomes a clean list.

## First list, captured fast

- Bike Reserved
- Reservation Updated
- Ride Started
- Ride Ended
- Ride Cost Calculated
- Bike Saved
- Card Charged
- Charge Failed
- Ride Start Refused
- Reservation Expired
- Bike Reported Damaged
- Damage Report Received

## Review of each weak entry

- Reservation Updated: a record change, not a business moment. The person says that the rider can move the start time. The event becomes "Reservation Rescheduled".
- Ride Cost Calculated: a computed value. The cost belongs in a read model built from the ride times and the price.
- Bike Saved: a database word. The person says that staff put a new bike at a station. The event becomes "Bike Added To Fleet".
- Damage Report Received: means the same as "Bike Reported Damaged". Keep one, and record the merge as a decision.
- Ride Start Refused: the business keeps a log of refused starts for fraud review. It stays as an event with the reason.
- Charge Failed: the business follows up on each failed charge. It stays as an event.

A rule with no record: "a rider with an open debt cannot reserve". The business keeps no record of the refusal. It is no event. The report names the rule.

## Clean list with key facts

- Bike Added To Fleet: bikeId, stationId.
- Bike Reserved: reservationId, bikeId, riderId, endsAt.
- Reservation Rescheduled: reservationId, endsAt.
- Reservation Expired: reservationId.
- Ride Started: rideId, bikeId, riderId, startedAt.
- Ride Start Refused: riderId, bikeId, reason.
- Ride Ended: rideId, stationId, endedAt.
- Card Charged: rideId, amount.
- Charge Failed: rideId, reason.
- Bike Reported Damaged: bikeId, riderId, description.

The amount on "Card Charged" is a captured fact. It is the amount that the card processor took, not a total that this system computes from other events.

## In an .em.hcl model

The ride identifier is made when the system records the fact, so it has `generated = true`. The rider and the bike come from the command that produces the event, so they have no `generated`.

```hcl
bounded_context "rental" {
  field_type "ride_id" {
    type         = "UUID"
    id_attribute = true
  }

  event "ride_started" {
    field "ride_id" {
      type      = field_type.ride_id
      generated = true
    }
    field "bike_id" {
      type = "String"
    }
    field "rider_id" {
      type = "String"
    }
    field "started_at" {
      type = "DateTime"
    }
  }

  event "ride_start_refused" {
    field "rider_id" {
      type = "String"
    }
    field "bike_id" {
      type = "String"
    }
    field "reason" {
      type = "String"
    }
  }
}
```
