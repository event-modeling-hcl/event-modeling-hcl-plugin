# Mapping example: a payment provider

The provider sends "charge.succeeded" with its own charge identifier. Our command "Start Rental" stored that identifier with the rental number when it started the charge.

## Payload

```json
{ "id": "ch_3Px9", "amount": 1250, "currency": "eur", "created": 1767268800 }
```

## Mapping to "Rental Paid"

| Payload field | Business field | Note |
| --- | --- | --- |
| id | charge reference | Plain field, duplicate key |
| amount | amount paid | 1250 cents is 12.50 EUR. Copy the unit rule from the provider document. |
| currency | currency | Upper case |
| created | paid at | Seconds to date and time |
| (none) | rental number | Enrich: look up by charge reference in our own data. Correlation key. |
| (none) | rider number | Enrich: from the rental |

Pattern: correlation lookup.

Failure cases for the translation command: no rental for the charge reference, rental already paid, the same charge delivered twice, amount below zero.

## In an .em.hcl model

```hcl
automation "record_rental_payment" {
  field_source {
    inputs = [event.payment_provider.charge_succeeded.field.id]
    target = command.record_rental_payment.field.charge_reference
  }
}
```

The command field `charge_reference` carries `deduplication_key = true`, and `rental_number` carries `correlation_key = true`.
