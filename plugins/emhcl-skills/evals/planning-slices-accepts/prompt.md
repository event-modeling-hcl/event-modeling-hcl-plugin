---
description: Slice report and status for a small library loan model.
tags: [method, delivery]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Here is our library loan model. Plan the slices. For each slice, tell me what it uses and produces, which slices come before and after it, its contract, and the status you give it. Do not write files. Answer in the reply.

```hcl
board {
  workflows = [
    workflow.borrow_book,
    workflow.open_loans,
    workflow.return_book,
  ]
}

actor "member" {
  auth_required = true
}

actor "librarian" {
  auth_required = true
}

bounded_context "lending" {
  aggregate "loan" {
    identity = field_type.loan_id
  }

  field_type "loan_id" {
    type = "UUID"
  }

  event "book_borrowed" {
    aggregate = aggregate.loan
    fields    = [field_type.loan_id]

    field "book_id" {
      type = "String"
    }

    field "due_date" {
      type = "Date"
    }
  }

  event "book_returned" {
    aggregate = aggregate.loan
    fields    = [field_type.loan_id]
  }
}

lifecycle "loan" {
  aggregate = aggregate.lending.loan

  state "open" {
    path = "main"
  }

  state "returned" {
    end  = true
    path = "main"
  }

  transition "borrow" {
    command = command.borrow_book.borrow_book
    events  = [event.lending.book_borrowed]
    before  = []
    after   = state.open
  }

  transition "return" {
    command = command.return_book.return_book
    events  = [event.lending.book_returned]
    before  = [state.open]
    after   = state.returned
  }

  invalid_transition "return_twice" {
    command = command.return_book.return_book
    before  = [state.returned]
    reason  = "A returned book cannot be returned again."
  }
}

state_change "borrow_book" {
  screen "borrow_desk" {
    actor = actor.member
    to    = [command.borrow_book]

    field "book_id" {
      type = "String"
    }
  }

  command "borrow_book" {
    to = [event.lending.book_borrowed]

    field "loan_id" {
      type      = field_type.lending.loan_id
      generated = true
    }

    field "book_id" {
      type = "String"
    }

    field "due_date" {
      type      = "Date"
      generated = true
    }
  }
}

state_view "open_loans" {
  readmodel "open_loans" {
    question = "Which loans are not returned yet?"
    from     = [event.lending.book_borrowed, event.lending.book_returned]
    to       = [screen.open_loans_page]

    field "loan_id" {
      type = field_type.lending.loan_id
    }

    field "book_id" {
      type = "String"
    }

    field "due_date" {
      type = "Date"
    }
  }

  screen "open_loans_page" {
    actor = actor.librarian

    field "loan_id" {
      type = field_type.lending.loan_id
    }

    field "book_id" {
      type = "String"
    }

    field "due_date" {
      type = "Date"
    }
  }
}

state_change "return_book" {
  screen "return_desk" {
    actor = actor.member
    to    = [command.return_book]

    field "loan_id" {
      type = field_type.lending.loan_id
    }
  }

  command "return_book" {
    to = [event.lending.book_returned]

    field "loan_id" {
      type = field_type.lending.loan_id
    }
  }
}

hotspot "late_return_fee" {
  question = "Does a member pay a fee for a late return?"
  on       = command.return_book.return_book
}
```
