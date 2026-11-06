# Read model example: the rider page

The rider page shows a ride count and a list of past rides. A rider names these as two things, so they are two areas.

## Rider Ride Count

- Query: the number of finished rides of one rider.
- Freshness: a few seconds.
- Fields: rider number (from Ride Ended), ride count (computed here: the count of Ride Ended).
- Rationale: Ride Ended adds one to the count.

## Rider Past Rides

- Query: the finished rides of one rider, newest first.
- Freshness: a few seconds.
- Fields: ride number, bike number, start time (from Ride Started), end time (from Ride Ended).
- Rationale: Ride Started adds the row with the bike and the start time. Ride Ended sets the end time.

## A split under the computation kind test

A first draft had one read model "Rider Page" with both areas. The count needs one event. The list needs two events. The fields have two kinds of computation, so the read model splits.

## In an .em.hcl model

```hcl
state_view "rider_past_rides" {
  readmodel "rider_past_rides" {
    question    = "Which rides did this rider finish, newest first?"
    description = "Ride Started adds the row. Ride Ended sets the end time."
    from        = [event.rental.ride_started, event.rental.ride_ended]
    to          = [screen.rider_page]

    field "ride_number" {
      type = "String"
    }
  }

  screen "rider_page" {
    actor = actor.rider
  }
}
```
