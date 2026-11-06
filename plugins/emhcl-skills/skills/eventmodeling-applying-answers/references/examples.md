# Examples of answers and their records

The domain is a gym that books fitness classes. Mia, the gym manager, answered.

## A rule answer

Question (rule) on Book Class: When must a booking be refused?
Answer: When the class already has 12 people.
Records: a decision "A class takes at most 12 people", source Mia. A request on Book Class, concerning command scenarios: given 12 Class Booked facts for class Y-3, when Book Class for Y-3, then refused with "This class is full". The question is resolved.

## A data answer

Question (data) on the booking form: Which details does the gym keep?
Answer: The member number and the class. The phone number is only for the reminder.
Records: a decision. A request on Book Class, concerning commands: fields member number and class. A request on Book Class, concerning automations: the reminder needs the phone number.

## A next answer that adds a step

Question (next) on Booking Confirmed: What happens after this?
Answer: The member pays at the desk before the class.
Records: a decision. A request on the event Booking Confirmed, concerning events and story order: a new step Pay at Desk after the booking. The booking step stays as it is.

## A view answer

Question (view) on My Classes: Which message appears for an empty list?
Answer: The text "No classes booked yet" and a link to the timetable.
Records: a decision. A request on the read model My Classes, concerning read model scenarios: no Class Booked fact exists, and the list is empty.

## A contradiction

Question (example) on Cancel Booking: Give a case where a cancel goes through.
Answer: A member cancels ten minutes before the class.
The model has a scenario that refuses a cancel later than one hour before the class.
Records: none. Question back with options: keep the one-hour limit, change it to ten minutes, or leave it.

## In an .em.hcl model

```hcl
hotspot "class_capacity" {
  category = "rule"
  question = "When must a booking be refused?"
  status   = "resolved"
  on       = command.book_class.book_class
}

evidence_source "mia" {
  kind     = "person"
  location = "Mia, gym manager, answers of 2026-11-04"
}

decision "class_capacity_twelve" {
  statement = "A class takes at most 12 people."
  reason    = "Answer of Mia to the question class_capacity."
  on        = command.book_class.book_class
}

evidence "class_capacity_answer" {
  certainty = "stated"
  source    = evidence_source.mia
  location  = "answer to the question class_capacity"
  on        = decision.class_capacity_twelve
}

hotspot "class_capacity_scenario" {
  kind     = "request"
  concerns = "scenario"
  question = "Can Book Class get a limit scenario: 12 bookings for Y-3, then Book Class for Y-3 is refused with This class is full (decision class_capacity_twelve)?"
  on       = command.book_class.book_class
}
```
