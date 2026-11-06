---
type: llm
---
PASS if the summary is the description of the chapter "renting" in rental.em.hcl and has every section in this order: What this chapter covers, Dates and deadlines, Business rules, Requirements and deliverables, Data and documents, Elements, Read model reasons, Integration gaps, Corrections, Open questions and risks, Assumptions, Not modeled, with "None" under each empty section (an overview above them is allowed), AND each number in it matches the model exactly (at most 3 open rentals) and names where it comes from (the scenario rider_with_three_open_rentals_is_refused or the element Start Rental). FAIL if a section is missing or out of order, an empty section is dropped instead of saying "None", the limit 3 is changed, or a summary file exists beside the model.
