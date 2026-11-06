---
description: Acceptance of applying answers on a small inline input.
tags: [method, evolution]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Mia (gym manager) answered our open questions. Apply her answers to the model below.

```hcl
hotspot "class_capacity" {
  category = "rule"
  question = "When must a booking be refused?"
  on       = command.book_class.book_class
}

hotspot "cancel_example" {
  category = "example"
  question = "Give a case where a cancel goes through."
  on       = command.cancel_booking.cancel_booking
}

hotspot "reminder_time" {
  category = "time"
  question = "When does the reminder go out?"
  on       = command.book_class.book_class
}
```

The model also has a scenario on Cancel Booking that refuses a cancel later than one hour before the class.

Answers of Mia:
- class_capacity: When the class already has 12 people.
- cancel_example: A member cancels ten minutes before the class.
- reminder_time: (no answer)
