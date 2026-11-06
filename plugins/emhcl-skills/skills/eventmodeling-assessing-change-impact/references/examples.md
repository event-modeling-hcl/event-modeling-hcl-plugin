# Example of a change assessment

The model in this example describes a city bike service. The person asks: "We want a deposit for day rentals. What does that change?" The model has no deposit yet.

The change lands first in Start Rental, because the rental type enters there. Downstream, Rental Started feeds Active Rental and the automation that ends a rental. Upstream, the rider already gives all the data that the change needs. The deposit itself needs three new slices.

## The result

1. Deposit for day rentals: 6 slices, 2 exist, 1 changes, 3 are new.
2. Summary: A rider who starts a day rental now pays a deposit first. An automation asks the payment provider to hold the deposit and later releases it when the rental ends. A new view shows the rider each deposit.
3. Start Rental (changed). The rider now chooses between an hour rental and a day rental.
   - Change: add the field rentalType (hour or day) to the screen, to the command Start Rental, and to the event Rental Started.
   - Change: new scenario. A day rental for a rider with an unpaid rental is rejected.
   - Rule: a bike that is under repair cannot be rented.
4. Hold Deposit (new, automation). Proposed: an automation picks up each day rental that has no deposit yet. It issues Hold Deposit, and the system records Deposit Held. Open question: the model does not state the deposit amount. Open question: the model does not say what happens when the payment provider refuses the hold.
   - Sketch: todo list Day Rentals Awaiting Deposit with rentalId and riderId.
   - Sketch: automation Hold Deposit For Day Rental.
   - Sketch: command Hold Deposit with rentalId, riderId, and amount.
   - Sketch: event Deposit Held with rentalId, amount, and heldAt.
5. Active Rental (existing). The rider still sees the running rental. The deposit does not appear in this view.
6. End Rental When Docked (existing). The automation ends the rental as before. Rental Ended is the event that the next new slice reads.
7. Release Deposit (new, automation). Proposed: when a day rental ends, an automation releases its deposit.
   - Sketch: todo list Ended Rentals With Held Deposit with rentalId and amount.
   - Sketch: automation Release Deposit After Rental.
   - Sketch: command Release Deposit with rentalId and amount.
   - Sketch: event Deposit Released with rentalId and releasedAt.
8. Rider Deposits (new, state view). Proposed: the rider sees each held and released deposit.
   - Sketch: read model Rider Deposits with rentalId, amount, heldAt, and releasedAt, fed by Deposit Held and Deposit Released.
   - Screen: a heading "My deposits" and a table with the headings Rental, Amount, Held on, and Released on.
   - Screen example data: rental R-2207, 80.00 EUR, 12 June, 13 June.
   - Screen example data: rental R-2251, 80.00 EUR, 19 June, not released.

## Why the example looks like this

- The steps follow the flow. The new slices sit between the existing ones and are not grouped at the end.
- The amount 80.00 EUR is only example data on a proposed screen. It is not a rule, so the deposit amount stays an open question.
- Customer Support View shows rentals too, but the person does not expect a change there. The assessment leaves it out.
