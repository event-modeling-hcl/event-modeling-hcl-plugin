# Example: options from a trail

A reviewer tried a library prototype. The comment on the "Borrow book" button says "this is wrong".

The trail shows five Book Borrowed events for one member. The last interaction is a click on "Borrow book".

The comment names no result, so it is ambiguous. Offer these options:

1. Refuse a sixth loan. Given five Book Borrowed events for member M-7. When Borrow Book for M-7. Then refused with "You can borrow at most 5 books".
2. Refuse a borrow without a member card. Given no Member Registered event for M-7. When Borrow Book for M-7. Then refused with "Register first".
3. Change only the button text to "Borrow this book".
4. Leave it.

If the person picks option 1, write a request on Borrow Book concerning command scenarios, with that scenario. Ask no further question.

# Example: a new step

A comment on "Place Order" says "ask for the delivery address first, then show the order total".

This adds a step. Request a new slice "Enter Delivery Address" right before "Place Order", with its own screen, command, and event. Request the order total as a field of a read model that the "Place Order" screen shows. Do not request a second command on the "Place Order" screen.

# Example: a merge request comment without a trail

The comment is on `model/ordering.em.hcl` line 42, inside `screen "checkout"`. It says "Label: Delivery date, not Ship date".

The comment names its result, so it is clear. The anchored line names the field `ship_date` of the screen Checkout.

## In an .em.hcl model

```hcl
evidence_source "mr_57_review" {
  kind     = "person"
  location = "merge request 57, comment of Sam on model/ordering.em.hcl:42"
}

decision "delivery_date_label" {
  statement = "The checkout screen shows the label Delivery date."
  reason    = "Review comment of Sam on merge request 57."
  on        = screen.place_order.checkout
}

hotspot "delivery_date_label_change" {
  kind     = "request"
  concerns = "screen"
  question = "Can the field ship_date on Checkout carry the title Delivery date (decision delivery_date_label)?"
  on       = screen.place_order.checkout
}
```
