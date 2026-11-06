# Example of an explained flow

The model in this example describes a city bike service. The person asks: "How does renting a bike work?" The chapter "Renting" holds the whole flow.

The outline shows six slices in the chapter. Four of them belong to the flow. The slice "Bike Docked From Station" is a translation step. It turns a message from the station hardware into the domain event Bike Docked. The flow ends with the receipt, so the explanation stops there.

## The result

1. Renting a bike: 4 slices.
2. Summary: A rider picks a free bike at a station and starts a rental with the bike number. The phone of the rider shows the running rental. When the rider docks the bike, the system ends the rental and shows the price.
3. Start Rental. The rider enters the bike number on the station screen and taps Start. The system records Rental Started with the bike, the rider, and the start time. The bike leaves the list of free bikes.
   - Rule: a rider with an unpaid rental cannot start a new rental.
   - Rule: a bike that is under repair cannot be rented.
4. Active Rental. The phone of the rider shows the bike number and the minutes since the start. The view changes when Rental Ended arrives.
   - Rules: none.
5. End Rental When Docked. The station reports Bike Docked, an event from another system. The automation picks up each docked bike that has an open rental and ends that rental. The system records Rental Ended with the end time. Open question: the model does not say what happens when a bike stays out for more than 24 hours.
   - Rule: a rental ends only at a station that accepted the bike.
6. Rental Receipt. The rider sees the duration and the price of the finished rental.
   - Rule: the first 45 minutes cost 1.20 EUR.
   - Rule: each further started 15 minutes costs 0.60 EUR.

## Why the example looks like this

- The explanation leaves out the translation slice. The person does not see it, and it adds nothing to the question about renting. Step 5 names Bike Docked as an event from another system.
- The open question in step 5 comes from a missing scenario. The explanation does not invent a rule for long rentals.
- The prices come from the scenarios of Rental Receipt, with the exact amounts.
