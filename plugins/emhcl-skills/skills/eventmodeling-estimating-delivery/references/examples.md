# Worked example: estimate for a library loan

A sprint lasts two weeks. The Lending team finished 3 weighted slices per sprint in each of its last four sprints. The Notifications team is new. The person gives no history for it.

## Slices and weights

| Slice | Kind | Owner team | Upstream | Weight |
| --- | --- | --- | --- | --- |
| Borrow Book | state change | Lending | none | 1 (typical: two rules) |
| Open Loans | state view | Lending | Borrow Book, Return Book | 0.5 (simple: three fields) |
| Return Book | state change | Lending | Borrow Book | 1 (typical) |
| Overdue Reminder | automation | Notifications | Borrow Book, Return Book | 2 (complex: an external mail service) |
| Pay Late Fee | state change | Lending | Return Book | 2 (complex: the card provider) |

Size: 1 + 0.5 + 1 + 2 + 2 = 6.5 weighted slices.

## Velocity

- Lending: 3 weighted slices per sprint. Source: the last four sprints.
- Notifications: 2 weighted slices per sprint. Source: assumed. The person confirms it after the first sprint.

## Phases

| Phase | Slices | Team load | Time |
| --- | --- | --- | --- |
| 1 | Borrow Book, Open Loans (contract only on Borrow Book and Return Book) | Lending 1.5 / 3 = 0.5 | 0.5 sprint |
| 2 | Return Book, Overdue Reminder | Lending 1 / 3 = 0.33, Notifications 2 / 2 = 1 | 1 sprint |
| 3 | Pay Late Fee | Lending 2 / 3 = 0.67 | 0.67 sprint |

Open Loans joins phase 1 because it needs only the postconditions of Borrow Book and Return Book. Its tests use sample events.

## Time

- Slices: 0.5 + 1 + 0.67 = 2.17 sprints.
- Work outside slices: 0.5 sprint, as the person states.
- Total: 2.67 sprints, or 5.33 weeks. Rounded up to whole weeks: 6 weeks.

## Capacity options

| Option | New velocity | Phase 2 | Total |
| --- | --- | --- | --- |
| One more developer in Notifications | Notifications 3 (assumed) | 0.67 sprint | 2.33 sprints, rounded up to 5 weeks |
| Faster delivery pipeline for Lending | Lending 4 (assumed) | 1 sprint (Notifications still decides) | 2.38 sprints, rounded up to 5 weeks |

## Assumptions

- The velocity of Notifications is assumed.
- Each new velocity in the capacity options is assumed.

## In an .em.hcl model

Each workflow is one slice. Its kind is the block type, its owner is `owner`, and its status is `status`. A workflow with `status = "done"` or `status = "informational"` is not part of the remaining work.

```hcl
state_change "borrow_book" {
  owner  = team.lending_team
  status = "planned"

  screen "borrow_desk" {
    actor = actor.member
    to    = [command.borrow_book]
  }

  command "borrow_book" {
    to = [event.lending.book_borrowed]
  }
}
```

The upstream slices of `borrow_book` are the workflows whose commands produce the events that it uses. The `from` lists of read models and todo lists name those events directly.
