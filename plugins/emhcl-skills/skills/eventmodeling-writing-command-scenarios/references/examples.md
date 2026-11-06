# Command scenario examples

The domain is a city bike rental. A rider starts a rental, ends it, and pays a fee.

## Success

Title: A rider starts a rental on a free bike

- Given: Bike Docked (bike B-71, station Harbor, at 08:40)
- When: Start Rental (rider Ana Ruiz, bike B-71, at 09:00)
- Then: Rental Started (rental R-502, rider Ana Ruiz, bike B-71, at 09:00)

## Rejection from a wrong state

The bike lifecycle has a refused move: a bike in use cannot start a second rental.

Title: A bike in use cannot start a second rental

- Given: Rental Started (rental R-502, bike B-71, at 09:00)
- When: Start Rental (rider Ben Ota, bike B-71, at 09:05)
- Then: no event
- Error: "This bike is already in use"

## Rejection of the input itself

Title: A rental cannot end before it starts

- Given: Rental Started (rental R-502, at 09:00)
- When: End Rental (rental R-502, at 08:55)
- Then: no event
- Error: "The end time is before the start time"

## Repeated business action

Title: An ended rental cannot end again

- Given: Rental Started (rental R-502, at 09:00), Rental Ended (rental R-502, at 09:30)
- When: End Rental (rental R-502, at 09:45)
- Then: no event
- Error: "This rental has already ended"

## Limit, both sides

The source says a rental over 120 minutes pays a late fee of 5 euros.

Title: A rental of 119 minutes pays no late fee

- Given: Rental Started (rental R-610, at 10:00)
- When: End Rental (rental R-610, at 11:59)
- Then: Rental Ended (rental R-610, minutes 119, late fee 0 euros)

Title: A rental of 121 minutes pays the late fee

- Given: Rental Started (rental R-611, at 10:00)
- When: End Rental (rental R-611, at 12:01)
- Then: Rental Ended (rental R-611, minutes 121, late fee 5 euros)

## Compensation

Title: A refund reverses a double charge

- Given: Fee Charged (rental R-502, 3 euros, at 09:31), Fee Charged (rental R-502, 3 euros, at 09:32)
- When: Refund Fee (rental R-502, 3 euros, reason "double charge")
- Then: Fee Refunded (rental R-502, 3 euros)

## Weak and strong wording

A weak scenario says "given a rental, when it ends, then it works". It names no state, no actor, and no result.

A strong scenario says "given a rental that started at 09:00, when the rider ends it at 09:30, then Rental Ended records 30 minutes".

## In an .em.hcl model

The rejection from a wrong state, inside the `state_change` workflow of the command. The refused move `bike_in_use` of the bike lifecycle names the same command.

```hcl
scenario "bike_in_use_cannot_start_second_rental" {
  title = "A bike in use cannot start a second rental"
  case  = "state_violation"

  given {
    event    = event.rental.rental_started
    examples = [{ rental_id = "R-502", bike_id = "B-71", started_at = "09:00" }]
  }

  when {
    command  = command.start_rental
    examples = [{ rider = "Ben Ota", bike_id = "B-71", requested_at = "09:05" }]
  }

  then {
    error = "This bike is already in use"
  }
}
```

The upper side of the late fee limit:

```hcl
scenario "rental_of_121_minutes_pays_late_fee" {
  title = "A rental of 121 minutes pays the late fee"
  case  = "limit"

  given {
    event    = event.rental.rental_started
    examples = [{ rental_id = "R-611", started_at = "10:00" }]
  }

  when {
    command  = command.end_rental
    examples = [{ rental_id = "R-611", ended_at = "12:01" }]
  }

  then {
    event    = event.rental.rental_ended
    examples = [{ rental_id = "R-611", minutes = 121, late_fee_euros = 5 }]
  }
}
```
