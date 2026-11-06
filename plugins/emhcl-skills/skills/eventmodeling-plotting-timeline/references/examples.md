# Timeline example: Renting a Bike

Use this example to see predecessors, triggers, decision points, and undo steps in one chapter.

## Timeline

1. Bike Reserved. Starts the path. Trigger: Rider. Precondition: the bike is free and the rider has no open debt.
2. Ride Started. After Bike Reserved. Trigger: Rider. Precondition: the reservation is still open.
3. Ride Ended. After Ride Started. Trigger: Rider. Precondition: the ride is open and the bike is at a station.
4. Card Charge Requested. After Ride Ended. Trigger: the end of the ride. Precondition: the ride is ended and not paid.
5. Card Charged. Handover from the Card Processor. After Card Charge Requested.
6. Ride Paid. After Card Charged. Trigger: the handover. End state: ride paid.

## Decision points

After Bike Reserved:

- Path A: the rider starts the ride. Go to Ride Started.
- Path B: time runs out. Reservation Expired. End state: reservation expired.

After Card Charge Requested:

- Path A: Card Charged, then Ride Paid.
- Path B: Charge Failed, a handover from the Card Processor. Then Rider Debt Recorded. End state: debt open.

## Undo steps

The person says that a ride paid twice gets a refund. The model has no refund event. Write a request concerning `event` for "Refund Given" after Ride Paid. End state: refund given.

## A branch that starts a different story

The person says that guests rent with a card at each ride and see other screens. That branch starts a different story. Do not plot it here. Write a request concerning the chapters part on its first element.

## In an .em.hcl model

The board lists the workflows in business time. Triggers and preconditions go into the workflow description. This fragment shows only the board and one request. The workflows that it names exist elsewhere in the model.

```hcl
board {
  workflows = [
    workflow.reserve_bike,
    workflow.start_ride,
    workflow.end_ride,
    workflow.charge_ride,
    workflow.record_charge_result,
  ]
}

hotspot "guest_branch" {
  kind     = "request"
  concerns = "chapter"
  question = "Guests rent with a card at each ride and see other screens. Does this start its own chapter?"
  on       = workflow.pay_as_guest
}
```
