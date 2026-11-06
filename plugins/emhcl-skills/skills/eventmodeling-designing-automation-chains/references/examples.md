# Automation chain example: charging a ride

A partner app reports that a ride ended. The business then charges the rider.

## Translation step

- Trigger: "Ride Ended" from the partner app (event from another system).
- Todo list: Partner Rides To Record. The external event opens an item. Nothing closes it.
- Command: Record Ride End. It decides nothing.
- Internal event: Ride Ended. The external name already is the business term, so it stays. "Ride End Received" is wrong.

## Worker step

- Todo list: Rides To Charge. Fields: ride number, rider number, minutes. "Ride Ended" opens an item. "Ride Charged" closes it.
- Command: Charge Ride. It computes the fee from the minutes and the tariff. That is a new decision.
- Result event: Ride Charged.

## Derived condition

"Rider In Debt" follows when a charge fails. A domain expert names it, and the reservation step reacts to it. It gets its own event, produced by an automation whose todo list "Charge Declined" opens.

## Review

| Question | Translation | Worker |
| --- | --- | --- |
| Reads its own todo list | yes | yes |
| Internal events open it | not required | yes |
| No closing event | yes | not required |
| New decision | not required | yes |
| Own result closes it | not required | yes |
| No status field | yes | yes |

## In an .em.hcl model

```hcl
automation "charge_ride" {
  readmodel "rides_to_charge" {
    question = "Which ended rides are not charged yet?"
    from     = [event.rental.ride_ended, event.billing.ride_charged]
    to       = [processor.ride_charger]

    field "ride_number" {
      type = "String"
    }
  }

  processor "ride_charger" {
    to = [command.charge_ride]
  }

  command "charge_ride" {
    to = [event.billing.ride_charged]
  }
}
```
