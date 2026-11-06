---
type: llm
---

The model has three elements that need a slice: the command borrow_book, the read model open_loans, and the command return_book.

PASS if both conditions hold:
1. The reply lists each of these three elements in exactly one slice (Borrow Book as a state change, Open Loans as a state view, Return Book as a state change), adds no slice for an element that the model does not have, and does not merge two elements into one slice.
2. Each of the three slices states its events used, its events produced, its upstream slices, its downstream slices, a precondition, and a postcondition. Return Book uses Book Borrowed and has Borrow Book upstream. Open Loans uses Book Borrowed and Book Returned and has Borrow Book and Return Book upstream.

FAIL if a slice is missing, a slice holds two elements, the reply invents a new event, command, or read model, or any slice lacks one of the six parts in condition 2.
