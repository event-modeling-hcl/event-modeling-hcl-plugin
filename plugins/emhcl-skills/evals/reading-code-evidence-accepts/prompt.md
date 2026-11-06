---
description: Acceptance of code evidence reading on a small inline input.
tags: [method, intake]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Read this code as evidence for an event model of the rental journey. The code root is rental-app/ at commit 9ab12cd. Here is the model so far and the relevant code. Do not stop for questions.

```hcl
bounded_context "rental" {
  event "bike_rented" {
    field "rental_id" { type = "string" }
  }
}
```

```kotlin
// src/rental/RentalHandler.kt
40  @PostMapping("/rentals")
41  fun startRental(req: StartRentalRequest): Rental {
42    require(bikes.status(req.bikeId) != "REPAIR") { "bike in repair" }
43    return store.insertRental(req.bikeId, req.riderId, clock.now())
44  }
97  @DeleteMapping("/rentals/{id}")
98  fun deleteRental(id: String) = store.delete(id)
```
```kotlin
// test/rental/RentalHandlerTest.kt
30  @Test fun rejectsWhenBikeInRepair() { ... }
```
