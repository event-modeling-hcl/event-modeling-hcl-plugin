# Sample coverage report

The chapter covers a car wash that sells wash passes.

| Slice | Coverage | Missing scenarios |
| --- | --- | --- |
| Buy Wash Pass | 60 | Reject a pass for a car that already holds one. Given car KL-204 holds a gold pass. When the driver buys a gold pass for KL-204. Then the purchase is rejected. Reject a pass for a car with unpaid washes. |
| Redeem Wash | 66 | Reject a wash on an expired pass. Given the pass of car KL-204 ended on March 1. When the driver redeems a wash on March 3. Then the wash is rejected. |
| Washes Left | 33 | A pass shows one wash less after a redeemed wash. A pass leaves the list when it expires. |
| Car Arrived From Gate | no value | The slice only hands over the gate signal. No business case can be derived. |

Three slices have a value. Average coverage: 53. Lowest three: Washes Left (33), Buy Wash Pass (60), Redeem Wash (66).

## The arithmetic

- Buy Wash Pass: 3 covered of 5 meaningful cases. 100 times 3 divided by 5 is 60.
- Redeem Wash: 2 of 3. 100 times 2 divided by 3 is 66.67. Round down: 66, not 67.
- Washes Left: 1 of 3. 33.33 rounds down to 33.
- Average: (60 + 66 + 33) divided by 3 is 53. Round down: 53.

## Cases that do not count

- Redeem Wash has a scenario "pass id is not a valid UUID". It is a technical case. It is not covered and not missing.
- Buy Wash Pass has two scenarios for the same gold pass purchase with other names. The second one repeats the first and counts once.
