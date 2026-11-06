# Example drift report

```
## Code drift: chapter "Room Booking"
Range: 4f2a91c (baseline) to 8d07be3. 4 commits. 3 behavior files.

### Fields
- [ ] Book Room (warning): the model says "guestCount". Commit 6b1c0aa "rename guests" by Ana renamed it to "partySize" in src/booking/BookingHandler.kt:33 and src/booking/RoomBooking.kt:12. Fix: rename the field on the command Book Room, the event Room Booked, the read model Booking Details, and the screens "Book a Room" and "My Booking". Parts: commands, events, read models, screens.

### Rules
- [ ] Book Room (critical): the model has a scenario that refuses a stay longer than 14 nights. Commit 8d07be3 "temp: skip max stay" by Leo disabled that test in test/booking/BookRoomTest.kt:58. Fix: restore the rule in the code, because the change looks accidental. The model does not change.

### Summary
The guest count field changed its name in code. The model still uses the old name. Rename it first.
Commits: 2c9e5d1 build Book Room (generated from the model), 6b1c0aa rename guests, 71f3a40 update dependencies, 8d07be3 temp: skip max stay
Not relevant: dependency file in 71f3a40
```

## In an .em.hcl model

After the person confirms the rename and declines the revert:

```hcl
hotspot "drift_party_size_command" {
  kind     = "request"
  concerns = "command"
  question = "Can the field guest_count on Book Room become party_size (commit 6b1c0aa, src/booking/BookingHandler.kt:33)?"
  on       = command.book_room.book_room
}

decision "max_stay_test_disabled" {
  statement = "The disabled max stay test in 8d07be3 stays as it is for now."
  reason    = "The person declined the revert. The scenario stays in the model."
  on        = command.book_room.book_room
}

evidence_source "code_pass_5" {
  kind        = "code"
  location    = "hotel-app/ at 8d07be3"
  description = "2026-11-06, pass 5, drift, scope: chapter room_booking. Result: one rename request, one declined finding (max stay test)."
}
```
