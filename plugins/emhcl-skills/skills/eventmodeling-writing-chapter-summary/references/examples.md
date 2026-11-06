# Example of a first-chapter summary

The model in this example comes from a fictional tender. The city of Northbridge asks for an operator of its bike service. The first chapter is "Renting and returning". All names, numbers, and dates are invented for this example.

## The summary

The text below is the content of the summary. It sits on the chapter as its summary.

```markdown
# City bike operation, Northbridge: overview

## Title and source
Tender "Operation of the Northbridge city bikes", file tender-main.pdf (42 pages) and annex-b.pdf (9 pages).
Perspective: the view of the bidding operator. This is an assumption, because the source does not name a reader.

## At a glance
The city looks for one operator for 600 bikes at 48 stations for four years.
The operator runs rentals, repairs, and customer support.
The city pays a fixed monthly fee and keeps the rental income.
The three points that matter most:
1. A station must never stay empty for more than 2 hours (tender-main.pdf, p. 14).
2. The operator pays a penalty for each missed repair deadline (p. 27).
3. The city owns all rider data (annex-b.pdf, p. 3).

## Go and no-go criteria
| Criterion | Threshold | Source |
| --- | --- | --- |
| Experience | At least 2 bike services with 300 bikes or more | p. 8 |
| Insurance | Liability cover of 5,000,000 EUR | p. 9 |

## Evaluation
| Criterion | Weight | Scoring |
| --- | --- | --- |
| Price | 40 % | Lowest price gets 100 points, others in proportion |
| Service concept | 35 % | 0 to 100 points by the panel |
| Repair plan | 25 % | 0 to 100 points by the panel |

## Dates for the whole document
| What | When | Source | Effect of a missed date |
| --- | --- | --- | --- |
| Bid deadline | 14 March 2027, 12:00 | p. 3 | The bid is excluded |

## Chapters
| Chapter | Purpose | Key elements |
| --- | --- | --- |
| Renting and returning | A rider takes and returns a bike | Start Rental, Rental Started, Rental Ended, Active Rental |
| Repairs | The operator fixes reported bikes | Report Defect, Repair Finished |

## Implementation notes
Build Renting and returning first, because Repairs reads Rental Ended.
A first thin slice is Start Rental with its screen and the event Rental Started.

# Renting and returning

## What this chapter covers
A rider starts a rental at a station and ends it by docking the bike.
The rider acts. The station hardware reports each docked bike.
Entities: rental (rentalId), bike (bikeNumber), rider (riderId).

## Dates and deadlines
None. The document-wide dates are in the overview.

## Business rules
| Rule | Held by | Scenario | Source |
| --- | --- | --- | --- |
| The first 45 minutes are free for subscribers | Rental Receipt | Free time for a subscriber | p. 18 |
| A rider with an unpaid rental cannot start a new one | Start Rental | Unpaid rental blocks a start | p. 19 |
The rule about unpaid rentals is a scenario with an error, not an event.

## Requirements and deliverables
| Item | Kind | Tracked by |
| --- | --- | --- |
| Live count of free bikes per station | Mandatory | Free Bikes At Station |
| Rental history for the rider | Optional | Rider Rentals |

## Data and documents
The monthly rental report to the city, with the number of rentals and the average duration (annex-b.pdf, p. 5).

## Elements
5 events, 2 commands, 4 read models, 1 automation, 3 screens.
Slices: 2 state changes (Start Rental, Return By Hand), 4 state views, 1 automation (End Rental When Docked).
External party: the station hardware, with the translated event Bike Docked.
Review result: PASS WITH WARNINGS.

## Read model reasons
Free Bikes At Station serves the station screen and the city report. It appears in both places as one read model.

## Integration gaps
The repair team needs the last rider of a damaged bike. Rental Ended carries the rider, but Repairs has no read model for it yet. Resolution options: a new read model in Repairs, or a field on Report Defect. See the open question "Who sees the last rider?".

## Corrections
Bike Docked moved before Rental Ended, because the first order suggested that the rental ended before the bike arrived.

## Open questions and risks
| Question or risk | Sources | Why it matters |
| --- | --- | --- |
| What happens when a bike stays out for more than 24 hours? | p. 19 | No end state for long rentals |
| The penalty has no upper limit | p. 27 | One-sided clause on penalties |

## Assumptions
A rental belongs to one rider only, because the source never mentions shared rentals.

## Not modeled
| Content | Reason |
| --- | --- |
| Marketing duties of the operator | Outside the scope of this chapter |
```

## Why the example looks like this

- The bid deadline applies to the whole tender, so it sits in the overview. The chapter refers to it.
- Each number has its page reference, and no number is rounded.
- The empty section "Dates and deadlines" stays and says "None".
- The summary sits on its chapter. No summary file exists beside the model.

## In an .em.hcl model

The summary is the `description` of the `chapter`, as a multi-line string. Only the start is shown.

```hcl
chapter "renting_and_returning" {
  title       = "Renting and returning"
  description = <<-EOT
    # City bike operation, Northbridge: overview

    ## Title and source
    Tender "Operation of the Northbridge city bikes", file tender-main.pdf (42 pages) and annex-b.pdf (9 pages).
    EOT
  workflows   = [workflow.start_rental, workflow.active_rental, workflow.end_rental_when_docked]
}
```
