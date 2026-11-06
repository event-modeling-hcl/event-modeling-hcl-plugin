# Sample stress test round

The chapter covers a farm box delivery service.

## Stressors and residues

- S1 (external). Heavy snow closes the roads. Residue: boxes get packed, but no box ships, and Delivery Planned stays open.
- S2 (internal). A farmer misses a weekly harvest. Residue: Box Packed lists items that do not exist, and customers learn it at the door.
- S3 (external). A new food labeling law starts. Residue: Box Contents shows no origin data, so no box can ship.
- S4 (internal). A customer moves in the middle of the week. Residue: Delivery Planned uses the old address.
- S5 (external). The main payment firm goes bankrupt. Residue: Subscription Renewed stops, and deliveries continue unpaid.

## Incidence matrix

| Element | Hits | Hit by |
| --- | --- | --- |
| Delivery Planned | 3 | S1, S2, S4 |
| Box Packed | 2 | S2, S3 |
| Box Contents | 1 | S3 |

Cluster: Delivery Planned and Box Packed share S2. The shared cause is that packing and planning both assume a fixed harvest.

## Redesign

Proposal: add a slice Report Harvest Shortfall and a todo list that swaps items before packing. New residue for S2: boxes ship with swapped items, and customers get told before delivery.

The person confirms. The skill writes two requests: one on the event Box Packed, concerning a new command, and one concerning a new automation with its todo list.

Residual index with a fresh set of 8 stressors: before 3 of 8 acceptable, after 6 of 8.

## In an .em.hcl model

```hcl
hotspot "harvest_shortfall_command" {
  kind     = "request"
  concerns = "command"
  question = "Can the farm report a harvest shortfall before packing, so that boxes do not list missing items?"
  on       = event.farm.box_packed
}
```
