---
type: llm
---

PASS if the response removes or splits the single "Fleet Activity" stream, and each resulting stream has one business identity of one thing (for example carId, reservationId or tripId, driverId), never a category such as "cars" or "activity", and each of the eight events is assigned to exactly one stream that it happened to. FAIL if "Fleet Activity" is kept as one stream, if a stream identity is a category, or if an event is missing or in two streams.
