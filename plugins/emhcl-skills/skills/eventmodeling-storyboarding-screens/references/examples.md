# Screen example: renting a bike and a damage report

This example shows one actor per stretch of the story, a real handoff, and planned read models.

## Rider stretch

Screen "Pick a Bike", for the Rider.

- Shows: station name, free bikes, price per minute. Source: Free Bikes At Station (planned read model, request written).
- Asks for: the chosen bike. It starts here.
- Action: reserve the bike.

Screen "My Reservation", for the Rider.

- Shows: bike number, station name, end time of the reservation. Source: Open Reservation (planned read model).
- Action: start the ride.

Screen "End Ride", for the Rider.

- Shows: start time, bike number. Source: Open Ride (planned read model).
- Action: end the ride.

Screen "Report Damage", for the Rider.

- Shows: bike number. Source: Open Ride.
- Asks for: a damage note. It starts here.
- Action: report damage.

The ride page holds two actions, so it gives two screens.

If the rider has an open debt, "Pick a Bike" says that a reservation is not possible until the debt is paid. The next step is the payment screen.

## Handoff to the Station Keeper

A damage report waits on staff. This is a real handoff.

Screen "Damaged Bikes", for the Station Keeper.

- Shows: bike number, station, damage note, report time. Source: Damage Reports To Handle (planned read model).
- Action: take the bike out of service.

## Not a screen

The card charge after the end of the ride runs with no person. It gets no screen.

## Role coverage

The Support Agent has no screen in this chapter. Ask the person whether the agent acts in another chapter. If not, write an open question.

## In an .em.hcl model

```hcl
state_change "reserve_bike" {
  screen "pick_a_bike" {
    title = "Pick a Bike"
    actor = actor.rider

    field "station_name" {
      type = "String"
    }

    field "bike_number" {
      type    = "String"
      example = "B-1042"
    }
  }
}

hotspot "free_bikes_read_model" {
  kind     = "request"
  concerns = "readmodel"
  question = "Pick a Bike shows free bikes and price per minute. Which read model supplies them?"
  on       = screen.reserve_bike.pick_a_bike
}
```

The commands part later adds the command and `to = [command.reserve_bike]` on the screen.
