# Worked example: slices of a library loan

The model has a member who borrows and returns a book, a librarian who sees the open loans, and an automation that reminds a member of an overdue loan.

## Elements

- The command Borrow Book produces the event Book Borrowed.
- The command Return Book produces the event Book Returned.
- The read model Open Loans shows each loan from Book Borrowed and removes it on Book Returned.
- The automation Overdue Reminder reads its todo list of overdue loans and issues the command Remind Member. Remind Member produces Member Reminded.

## Slices

Slice: Borrow Book
- Kind: state change.
- Element: the command Borrow Book. A member takes a book home.
- Events used: none. The command starts the loan stream.
- Events produced: Book Borrowed, when the book has no open loan.
- Upstream: none.
- Downstream: Return Book, Open Loans, Overdue Reminder.
- Precondition: the book has no open loan.
- Postcondition: Book Borrowed exists with the loan id, the book id, the member id, and the due date.
- Status: planned.

Slice: Return Book
- Kind: state change.
- Element: the command Return Book. A member brings a book back.
- Events used: Book Borrowed, to know that the loan is open.
- Events produced: Book Returned.
- Upstream: Borrow Book.
- Downstream: Open Loans, Overdue Reminder.
- Precondition: Book Borrowed exists for this loan, and no Book Returned exists.
- Postcondition: Book Returned exists with the loan id and the return date.
- Status: blocked. The open question "Does a member pay a fee for a late return?" is on the command.

Slice: Open Loans
- Kind: state view.
- Element: the read model Open Loans. The librarian sees each loan that is not returned.
- Events used: Book Borrowed adds a row. Book Returned removes it.
- Events produced: none.
- Upstream: Borrow Book, Return Book.
- Downstream: none.
- Precondition: none. An empty list is a valid view.
- Postcondition: one row for each open loan.
- Status: planned.

Slice: Overdue Reminder
- Kind: automation.
- Element: the automation Overdue Reminder. It reminds the member when the due date passes.
- Events used: Book Borrowed opens an item. Book Returned closes it.
- Events produced: Member Reminded.
- Upstream: Borrow Book, Return Book.
- Downstream: none.
- Precondition: an open loan with a due date in the past.
- Postcondition: Member Reminded exists with the loan id and the reminder date.
- Status: planned.

## Dependencies

| From | Event | To | Pattern |
| --- | --- | --- | --- |
| Borrow Book | Book Borrowed | Return Book | command to event to command |
| Borrow Book | Book Borrowed | Open Loans | command to event to read model |
| Return Book | Book Returned | Open Loans | command to event to read model |
| Borrow Book | Book Borrowed | Overdue Reminder | command to event to automation |
| Return Book | Book Returned | Overdue Reminder | command to event to automation |

The team of Open Loans can start at once. Its tests use a sample Book Borrowed event from the postcondition of Borrow Book.

## In an .em.hcl model

Each slice is one workflow. The status goes on the workflow. The open question stays a `hotspot` on the command, and the report names it as the reason for `blocked`.

```hcl
state_change "borrow_book" {
  status = "planned"

  screen "borrow_desk" {
    actor = actor.member
    to    = [command.borrow_book]
  }

  command "borrow_book" {
    to = [event.lending.book_borrowed]
  }
}

state_view "open_loans" {
  status = "planned"

  readmodel "open_loans" {
    question = "Which loans are not returned yet?"
    from     = [event.lending.book_borrowed, event.lending.book_returned]
    to       = [screen.open_loans_page]
  }

  screen "open_loans_page" {
    actor = actor.librarian
  }
}

state_change "return_book" {
  status = "blocked"

  screen "return_desk" {
    actor = actor.member
    to    = [command.return_book]
  }

  command "return_book" {
    to = [event.lending.book_returned]
  }
}

hotspot "late_return_fee" {
  question = "Does a member pay a fee for a late return?"
  on       = command.return_book.return_book
}
```

The events used by Return Book come from the lifecycle of the loan. Its move `return` has `before = [state.open]`, and the move `borrow` with the event `book_borrowed` leads to `state.open`.

A request for a status change looks like this. The skill resolves it before it reports done.

```hcl
hotspot "rebuild_return_book" {
  kind     = "request"
  concerns = "workflow"
  question = "The code no longer matches the return rule. Can Return Book go back to planned?"
  on       = workflow.return_book
}
```
