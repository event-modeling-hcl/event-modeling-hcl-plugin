---
type: llm
---
PASS if each stop in the table joins the journey through the same field (bike_number) or a declared origin, and no field that only sounds similar (such as rental_id) is a stop, AND each stop has exactly one role (origin, stored, transformed, used, or sent), the field name on that element, its slice, and a short note, with the Start Rental screen as origin and Rental Started and Bike Returned as stored. FAIL if a stop has no role or two roles, an element appears twice, rental_id or rider_phone appears as a stop for the bike number, or a stop is invented that the model does not have.
