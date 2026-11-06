---
type: llm
---
PASS if the explanation has one step for each slice, in the board order Start Rental, Active Rentals, Return Bike, and no step is about a single element or a single scenario, AND each rule it states comes from a scenario of its slice with the threshold exactly as the model states it (a rider can hold at most 3 open rentals), with no other rule invented. FAIL if the steps follow another order, a slice is split into several steps, a rule appears that no scenario states (for example a price or a return deadline), or the limit 3 is changed.
