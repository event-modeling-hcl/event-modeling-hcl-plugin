# Worked example: a run on a library loan model

The person asks: "Finish the model of our library loans." The model holds roles and events.

## Pass 1

Gate state:

| Gate | Result | Failing elements |
| --- | --- | --- |
| roles | pass | |
| events | pass | |
| chapters | fail | Book Borrowed and Book Returned have no chapter. |

Report line: "Gate chapters fails: Book Borrowed and Book Returned belong to no chapter. Loading the writer of chapters."

The run loads the skill whose description says that it writes chapters. It gives that skill the two events and the sources.

## Pass 2

Chapters and story order pass. The screens gate fails: the role Librarian has no screen. The run loads the skill whose description says that it writes screens.

## Pass 9

The reviews gate is the first gate that fails. The run loads each skill whose description says that it reviews the model and writes nothing. One review reports: "The screen Open Loans shows the due date, but no read model carries it." The person confirms the fix. The review writes it as a request on the read model Open Loans, concerning read models.

## Pass 10

The read models gate fails again, because an open request is on its part. The run loads the writer of read models. After its change, the gates up to reviews pass. The next review finds nothing new. The review loop stops.

## Final report

| Gate | Result |
| --- | --- |
| roles | pass |
| events | pass |
| chapters | pass |
| story order | pass |
| screens | pass |
| streams | pass |
| lifecycles | pass |
| commands | pass |
| automations | pass (no automation) |
| external mappings | pass (no event from another system) |
| read models | pass |
| command scenarios | pass |
| read model scenarios | pass |
| reviews | pass |
| slice status | pass |
| ownership | pass (teams do not matter to the person) |
| chapter summaries | pass |

- Stop rule: every gate passes.
- Open questions: "Does a member pay a fee for a late return?" on the command Return Book.
- Accepted debt: none.
- Facts that the model cannot hold: none.

## In an .em.hcl model

The gates run in the order of H3. Before each pass, the run reads the model and calls the validator:

```text
emhcl validate --profile workshop library.em.hcl
```

This model passes roles, events, streams, and lifecycle states. It fails screens, because no `screen` names `actor.librarian` or `actor.member`. The board is still empty.

```hcl
board {
  workflows = []
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
}
```

Report line: "Gate screens fails: the roles member and librarian have no screen. Loading the writer of screens."

Chapters and the board come later in H3, after the workflows exist. The run never adds a workflow to hold a chapter.

A request from a review makes an earlier gate fail again. This request fails the read models gate:

```hcl
hotspot "due_date_source" {
  kind     = "request"
  concerns = "readmodel"
  question = "The screen open_loans_page shows due_date. Can the read model open_loans carry it?"
  on       = readmodel.open_loans.open_loans
}
```
