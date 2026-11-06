---
type: llm
---
PASS if the reply lists about 15 stressors (12 to 18), at least 5 of them external (changes outside the model, in the business or its surroundings), with external and internal stressors alternating rather than grouped. Each stressor must have one residue that names slices or elements of the given model (such as Start Rental, Active Rentals, Return Bike, Rental Started) and no field name (such as rider_phone or bike_number). FAIL if fewer than 5 stressors are external, the stressors are grouped by kind, a residue names a field, or a residue names an element that the model does not have.
