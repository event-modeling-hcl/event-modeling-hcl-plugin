---
type: llm
---

The remaining slices are Register Member, Borrow Book, Return Book, Open Loans, and Charge Late Fee. Member Directory is done.

PASS if both conditions hold:
1. Each of the five remaining slices has exactly one weight in the plan, and Member Directory adds no weight to the size of the work.
2. No slice is in an earlier phase than one of its upstream slices: Borrow Book comes after Register Member, Return Book after Borrow Book, and Charge Late Fee after Return Book. Open Loans can share a phase with an upstream slice only when the plan marks that dependency as contract only.

FAIL if a remaining slice has no weight or two weights, if Member Directory counts in the size, if all slices run in one parallel phase, or if a slice is placed before one of its upstream slices without a contract-only mark.
