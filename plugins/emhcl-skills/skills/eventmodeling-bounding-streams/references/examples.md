# Worked stream examples

Each example names one thing, its identity, and the reason for the boundary.

## A library

A loan stream has the identity of one loan, such as loan L-2207. Its events are "Book Lent", "Loan Extended", and "Book Returned". The loan has one borrower and a natural end. The boundary is right.

A stream named "All Loans" receives "Book Lent" for every member. It has no single identity and never ends. It is a collection. Remove it, and write a request concerning the read models part for "Loans of a member".

A member stream holds "Member Joined", "Address Changed", "Reading List Item Added", and "Signed In At Kiosk". These are three concerns. Split them into a member profile stream, a reading list stream, and a kiosk session stream.

## A bank

A savings account stream with identity A-55031 holds deposits and interest for thirty years. Every event happened to this account. Keep it. Length is not a finding.

A transfer has its own short lifecycle: requested, approved, settled. Give it its own stream with the identity of one transfer. Do not fold it into the account stream.

A mortgage stream holds payments for twenty years. After the last payment, the record must stay for ten more years by law. The active mortgage and the closed record have different users and rules. Split them, and record the reason as a decision.

## A subscription service

A subscription stream with identity S-918 holds "Subscription Started", "Plan Upgraded", and "Subscription Ended". It has one owner and a clear lifecycle. The boundary is right.

A team space stream holds "Member Invited" and "Space Renamed". It also holds every "Document Opened" by every member. The document activity is a different concern with its own users. Move it to its own stream.

## A composite order

A furniture order with identity F-4410 holds three order lines and one delivery address. The lines start and end with the order. Keep them inside the order stream.

If an order line can be returned and refunded on its own schedule, the return has its own lifecycle. Give the return its own stream.

## In an .em.hcl model

The identity type exists in the context. Each event of the aggregate carries a field of that type.

```hcl
bounded_context "lending" {
  field_type "loan_id" {
    type         = "String"
    example      = "L-2207"
    id_attribute = true
  }

  aggregate "loan" {
    identity = field_type.loan_id
  }

  event "book_lent" {
    aggregate = aggregate.loan
    fields    = [field_type.loan_id]
  }

  event "book_returned" {
    aggregate = aggregate.loan
    fields    = [field_type.loan_id]
  }
}

hotspot "loans_of_member_view" {
  kind     = "request"
  concerns = "readmodel"
  question = "The stream All Loans was a collection and is removed. Add a read model that answers: which loans does this member have?"
  on       = aggregate.lending.loan
}
```
