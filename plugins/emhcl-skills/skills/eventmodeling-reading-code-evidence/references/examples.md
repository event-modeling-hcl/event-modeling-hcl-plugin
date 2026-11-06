# Worked example: a bike rental application

The code root is `rental-app/`. The pass is layer 1 for the journey "rent a bike" at commit `7c41e02`.

## Ledger table in the reply

| Lens | Code location | Hypothesis | Certainty | Record |
| --- | --- | --- | --- | --- |
| API | `src/rental/RentalHandler.kt:42` `RentalHandler#startRental`, `POST /rentals` | a screen where the rider starts a rental, and the command Start Rental | implied | requests concerning screens and commands |
| Persistence | `src/rental/RentalStore.kt:88` insert into `rentals` | the event Rental Started, with bike id, rider id, start time | implied | request concerning events |
| Tests | `test/rental/RentalHandlerTest.kt:30` `rejectsWhenBikeInRepair` | rule: a bike in repair cannot be rented | stated | request concerning command scenarios |
| User interface | `web/pages/bike-detail.html:12` button "Rent now" | the rider decides on the bike detail page | implied | evidence on the screen |
| Persistence | table `stations`, read in `src/station/StationQuery.kt:15`, never written | reference data | implied | open question: where does the station list come from? |

## A lens disagreement

The route `DELETE /rentals/{id}` exists in `src/rental/RentalHandler.kt:97`. No page and no test calls it. The skill writes an open question: "Can a rider cancel a rental after it starts?"

## The person outranks the code

The code allows a rental without a payment card. The person says that this never happens in the business. The skill writes a decision that records the code behavior at `src/rental/RentalHandler.kt:51`, and evidence with the person as source.

## In an .em.hcl model

```hcl
evidence_source "code_pass_3" {
  kind        = "code"
  location    = "rental-app/ at 7c41e02"
  description = "2026-11-02, pass 3, scope: chapter rent_bike (src/rental/, test/rental/). Result: five requests, two open questions."
}

evidence "rent_now_button" {
  certainty = "implied"
  source    = evidence_source.code_pass_3
  location  = "web/pages/bike-detail.html:12, button Rent now"
  on        = screen.start_rental.bike_detail
}

hotspot "bike_in_repair_rule" {
  kind     = "request"
  concerns = "scenario"
  question = "Can Start Rental get a scenario that refuses a bike in repair (test/rental/RentalHandlerTest.kt:30 rejectsWhenBikeInRepair)?"
  on       = command.start_rental.start_rental
}
```
