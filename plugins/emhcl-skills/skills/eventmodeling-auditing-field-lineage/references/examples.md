# Sample gap table

The model covers a bakery that takes cake orders. The audit covered the chapters Ordering and Kitchen, 42 fields.

| Element | Field | Gap | Search result | Status |
| --- | --- | --- | --- | --- |
| Order Cake (command) | pickup date | no consumer | Cake Ordered has no pickup date. No other event carries it. | outstanding |
| Order List (read model) | baker name | no origin | Baker Assigned in the Kitchen chapter carries "assigned baker". The read model does not take that event. | outstanding: real origin found, the link is missing |
| Cake Ordered (event) | price | no origin | The Price List read model on the order screen shows "cake price". The command does not carry it. | outstanding |
| Order Screen (screen) | cake name | no origin | The Cake Menu read model of the Ordering chapter carries "name" and the screen already maps it. | fixed |

Daily Totals has a field "cakes sold". It is a count from Cake Ordered, so it starts on the read model. It is not a gap and is not in the table.

Finding for Order Cake: the pickup date that the customer enters never reaches Cake Ordered. Evidence: Cake Ordered has the fields order id, cake, and customer only. Fix: add "pickup date" to Cake Ordered. Part: events. Severity: critical.

Verdict: FAIL.

## In an .em.hcl model

The customer types the pickup date on the screen. The screen is its origin, so the field has no `generated` and no `field_source`:

```hcl
screen "order_cake" {
  actor = actor.customer
  to    = [command.order_cake]

  field "pickup_date" {
    type = "Date"
  }
}
```

A system-filled value carries `generated = true`, such as the order identifier on the event. A renamed value has a `field_source` in the workflow of the target. A field with none of these and no same-named field upstream is a gap. After the person confirms the fix, the request is a hotspot on the event:

```hcl
hotspot "add_pickup_date" {
  kind     = "request"
  concerns = "event"
  question = "Can Cake Ordered carry the pickup date that the customer enters on Order Cake?"
  on       = event.ordering.cake_ordered
}
```
