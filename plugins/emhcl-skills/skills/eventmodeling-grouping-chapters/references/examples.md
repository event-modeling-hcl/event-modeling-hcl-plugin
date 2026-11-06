# Grouping example: a city bike rental

Use this example to see chapters that are too small and how to merge them.

## First proposal, too fine

1. Add Bike
2. Find Bike
3. Repair Bike
4. Reserve Bike
5. Start Ride
6. End Ride
7. Pay For Ride
8. Pay As Guest

## Review

- "Add Bike", "Find Bike", and "Repair Bike" are one verb and one noun each. They tell one journey of staff who keep the fleet working. Merge them into "Fleet Care".
- "Reserve Bike", "Start Ride", "End Ride", and "Pay For Ride" each start with what the one before made. They are one journey of a rider. Merge them into "Renting a Bike".
- A card charge that succeeds or fails is a decision point. Both results stay inside "Renting a Bike".
- "Pay As Guest" starts before the rental. A guest sees other screens, gives a card at each ride, and has no account. It is a divergent journey. Keep it as its own chapter, "Renting as a Guest".

## Final chapters

1. Fleet Care: a station keeper adds, moves, and repairs bikes.
2. Renting a Bike: a rider with an account reserves, rides, returns, and pays.
3. Renting as a Guest: a guest rents one bike with a card and no account.

## In an .em.hcl model

A chapter lists the workflows of its journey. These workflows already exist as slices. Each workflow is in one chapter only.

```hcl
chapter "renting_a_bike" {
  title     = "Renting a Bike"
  workflows = [
    workflow.reserve_bike,
    workflow.start_ride,
    workflow.end_ride,
    workflow.charge_ride,
  ]
}

chapter "fleet_care" {
  workflows = [workflow.add_bike, workflow.take_bike_out_of_service]
}

decision "merge_fleet_steps" {
  statement = "Add Bike, Find Bike, and Repair Bike form one chapter, Fleet Care."
  reason    = "They are one journey of staff who keep the fleet working."
}
```
