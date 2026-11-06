# Read model scenario examples

The domain is a city bike rental.

## Format decision

- Free Bikes at Station: storyline, because bikes arrive and leave all day.
- Rider Balance: storyline, because each top up and each fee changes the amount.
- Rental Receipt: view scenarios only, because one ended rental gives one receipt.
- Rider Profile: view scenarios only, because its source is the Sign Up chapter.

## View scenario with values

Title: The receipt shows the ended rental

- Given: Rental Ended (rental R-502, minutes 30, fee 3 euros)
- When: nothing
- Then: Rental Receipt (rental R-502, minutes 30, fee 3 euros)

## Empty list on purpose

Title: No free bikes after the last bike leaves Harbor

- Given: Bike Docked (bike B-71, station Harbor), Rental Started (bike B-71)
- When: nothing
- Then: Free Bikes at Station for Harbor, the list is empty

## Source in another chapter

Title: Rider Profile shows the name, fed from the Sign Up chapter

- Given: nothing in this chapter
- When: nothing
- Then: Rider Profile (rider Ana Ruiz, plan "Monthly")

## Storyline for an accumulating balance

1. Rider Balance for Ana Ruiz shows 0 euros.
2. After Balance Topped Up (20 euros), it shows 20 euros.
3. After Balance Topped Up (15 euros), it shows 35 euros.
4. After Fee Charged (3 euros), it shows 32 euros.

## Storyline with an error beat

1. Free Bikes at Station for Harbor is empty.
2. After Bike Docked (bike B-71), it lists B-71.
3. Start Rental for bike B-44 at Harbor is refused: "This bike is not at this station". The list still shows B-71.
4. After Rental Started (bike B-71), the list is empty.

A view scenario that says "after Bike Docked, the list shows B-71" repeats beat 2. Remove it.

## In an .em.hcl model

A view scenario in the `state_view` workflow of the read model. It has no `when` step.

```hcl
scenario "receipt_shows_ended_rental" {
  title = "The receipt shows the ended rental"
  case  = "appear"

  given {
    event    = event.rental.rental_ended
    examples = [{ rental_id = "R-502", minutes = 30, fee_euros = 3 }]
  }

  then {
    readmodel = readmodel.rental_receipt
    examples  = [{ rental_id = "R-502", minutes = 30, fee_euros = 3 }]
  }
}
```

An intentionally empty list:

```hcl
scenario "no_free_bikes_after_last_bike_leaves_harbor" {
  title = "No free bikes after the last bike leaves Harbor"
  case  = "disappear"

  given {
    event    = event.fleet.bike_docked
    examples = [{ bike_id = "B-71", station = "Harbor" }]
  }

  given {
    event    = event.rental.rental_started
    examples = [{ bike_id = "B-71" }]
  }

  then {
    readmodel         = readmodel.free_bikes_at_station
    expect_empty_list = true
  }
}
```

HCL has no storyline block. Write a storyline as one scenario per beat, each with the ordered `given` steps up to that beat. Write the first beat with `empty_history = true` and no `given` step.

A read model fed from another chapter still lists its feeding event in `from`. In HCL, its scenario names that event in a `given` step and says in `title` that the source is in that chapter. `empty_history = true` means "before any event", so never use it for this case.
