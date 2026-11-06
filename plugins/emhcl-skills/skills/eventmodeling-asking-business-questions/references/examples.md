# Examples of business questions

## Questions about a model

The model covers a dog daycare.

| Element | Category | Question |
| --- | --- | --- |
| Book Day Slot | rule | Can a booking fail? |
| Book Day Slot | example | What do we expect when an owner books a dog that has no vaccination record? |
| Book Day Slot | who | Who is allowed to book: only the owner, or also a family member? |
| Drop Off Dog | time | What happens when the dog arrives two hours after the booked time? |
| Pickup Reminder | rule | If the reminder service does not answer, does anyone still get told? |
| Front Desk screen | action | This screen lets staff start several different actions from one place. Which one does the person choose here? |

Weak questions to avoid:

- "No error event on Book Day Slot." This uses model words.
- "Is a welcome email missing?" Nothing in the model asks for one.
- "What is the booking ID format?" This is a technical field.

## A prototype tour

The domain is a small bakery that takes cake orders online. The model has three screens in this order: Choose Cake, Order Details, Order Received.

First pass, in story order:

1. Choose Cake, action: What happens when a customer clicks "Order this cake"?
2. Choose Cake, next: After the click, what does the customer see next?
3. Order Details, data: Which of these details does the bakery keep after the order?
4. Order Details, next: What happens after the customer sends the order? Is anyone at the bakery told?
5. Order Received, next: What does the customer do after this? What happens on the day before pickup?

Second pass, for risky elements:

6. Order Details, rule: When must the bakery refuse an order?
7. Order Details, example: Give one order that goes through and one that the bakery refuses.
8. Order Received, time: What if the customer does not collect the cake on the pickup day?

A question with a setup:

- Question: A customer orders a cake for tomorrow. Does the bakery accept it?
- Setup: Cake Chosen with pickup date 2026-06-02. The order date is 2026-06-01. Only the two dates decide the outcome. All other values stay empty.

## In an .em.hcl model

```hcl
hotspot "late_drop_off" {
  category = "time"
  question = "What happens when the dog arrives two hours after the booked time?"
  options  = ["Staff accept the dog.", "Staff refuse the dog and the day is charged."]
  on       = command.drop_off_dog.drop_off_dog
}
```
