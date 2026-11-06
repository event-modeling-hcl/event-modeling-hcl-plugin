---
name: eventmodeling-stress-testing-model
description: Stress tests one chapter of an event model with stressors from many directions, describes what is left after each one, and finds hidden coupling in an incidence matrix. It proposes redesigns as new slices and measures them with a fresh set of stressors. Use it when someone asks how the model survives things that go wrong in the world, such as "what breaks if the payment provider goes down?" or "stress test this chapter". Does not check the model against the modeling rules and does not change elements. Writes nothing until the person confirms a redesign, then writes requests only.
metadata:
  version: "1.0.0"
  contract: "K0 K3 K8 K9 K10 H0 H10"
---

# Stress testing the model

This skill shows what is left of a chapter when things go wrong. It finds elements that break together, proposes new slices for each such group, and measures the effect with fresh stressors. It writes nothing until the person confirms a redesign. Then it writes one request (K8) for each confirmed change.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

You read one chapter: its slices, elements, fields, and connections. Use only this reading for the whole round. If the person names no chapter and the model holds more than one, ask under K9.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

Terms:

- A stressor is anything that can happen to the business or its world: technical, legal, market, people, or nature. Far-fetched stressors are welcome.
- A residue describes the result of a stressor: the slices that remain usable and the data that remains or disappears. A proposed fix is not a residue.
- An incidence matrix is a table of stressors against elements. It shows which stressor hits which element.
- A cluster is a group of elements that the same stressors hit. A cluster shows hidden coupling.

## Procedure

1. Write about 15 stressors. At least 5 concern changes outside the model, such as changes in the business or its surroundings.
2. Take the rest from the business of the chapter, still at business level.
3. Alternate external and internal stressors in the list. Do not group them.
4. Write each stressor in at most eight words, as a business person says it.
5. Write one short residue for each stressor. Name the slices or elements it hits.
6. Show the list. Ask the person to mark each stressor whose residue is unacceptable.
7. If the person asks for more stressors first, keep the full list with its numbers. Add about 10 fresh ones and continue the numbering. Aim them at the elements and the kinds of stressor that the earlier list hit least.
8. When the person marks the unacceptable stressors, build the incidence matrix at once. For each marked stressor, list every element it hits. Use only the model you read. Never guess.
9. Write one line for each element that a stressor hits at least once. Sort by the number of hits, most first.
10. Name the clusters, the shared cause of each cluster, and the elements with the most hits.
11. If fewer than 5 stressors are marked, say that the coupling evidence is thin.
12. Ask the person which cluster to redesign first.
13. For that cluster, propose new slices of the kinds of K3. Examples are a translation step, a todo list that reconciles, a grace period, or a second way in. Describe the result after the redesign for every stressor that affects the cluster.
14. If the person confirms, write a request (K8) for each new slice or changed element, concerning the part that must change. Place it on the element where the change starts. If the person declines, offer the next cluster.
15. Write a fresh set of stressors that no earlier round used.
16. Ask the person to mark the unacceptable residues before and after the redesign.
17. Report the residual index: the acceptable residues before and after, out of the fresh set.
18. Repeat from step 12 until new stressors hit no new elements, or until the person stops.

## Rules

1. Write stressors and residues in business words. No field names, values, races, tokens, or system mechanics.
2. One stressor per line. No sub-lists of examples inside a stressor.
3. The number of directions that the stressors come from matters more than the choice of each stressor.
4. A residue names real slices and elements from the model. It never names a field.
5. Fields appear only in the matrix step.
6. A redesign stays a proposal until the person confirms it. A confirmed redesign becomes requests, never a direct change.

Read `references/examples.md` when you need a sample round.

## Result

Before the person confirms, the skill writes nothing. After a confirmation, it writes one request for each change, each on its element and naming its part.

It reports to the person: the stressor list with residues, the incidence matrix with its clusters, the redesign proposals with new residues, the requests it wrote, and the residual index of each round. If more than 10 stressors are marked, the matrix shows one "hit by" entry for each element instead of one mark for each stressor.

## Done when

1. About 15 stressors exist, at least 5 of them external, with external and internal stressors alternating.
2. Each stressor has one residue that names slices or elements of the model and no field.
3. The incidence matrix uses only the model and sorts the elements by hits.
4. Each cluster has a cause and a redesign proposal with new residues.
5. The report warns about thin evidence when fewer than 5 stressors are marked.
6. Each confirmed redesign is a set of requests on its elements, and no element changed.
7. A fresh stressor set gave a residual index.
8. The loop stopped because new stressors hit no new elements, or because the person stopped it.
