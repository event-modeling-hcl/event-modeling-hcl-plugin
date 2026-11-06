---
name: eventmodeling-grouping-chapters
description: Groups the model into chapters, one for each user journey from its start to its outcome, and names each chapter. Use it when someone asks to split a model into journeys or chapters, asks which process a step belongs to, or finds that a branch starts a different story. Writes chapters only. Does not write the order of steps inside a chapter, chapter summaries, or events.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K8 K9 H0 H3 H10"
---

# Grouping the model into chapters

This skill splits the model into chapters. It writes the chapters part (K0). A chapter is one user journey, told from its start to its outcome. Each event belongs to exactly one named chapter.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs:

- The events part and the roles part of the model.
- The chapters part, if it exists. Reuse a chapter when its journey matches.
- The open requests on the chapters part.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`. In an `.em.hcl` model a chapter holds workflows, not events (H3). Write chapters only when the slices exist. Until then, report the proposed journeys to the person and leave the chapters gate open.

## Procedure

1. Resolve each open request on your part first.
2. Read the events and find the business processes in them.
3. Put the events of one process into one group. A group is one story that a reader can follow alone.
4. Make sure that one team or one domain expert can own each group.
5. If all events form one short, straight flow, keep one chapter.
6. Name each chapter for its journey, for example "Renting a Bike" or "Fleet Care".
7. Read the names in order. Each name must tell a journey that someone lives through.
8. If a name is one verb and one noun, or names one form, merge that chapter with its neighbor.
9. If a chapter holds only one or two steps, merge it into the journey it belongs to.
10. If a chapter starts with the thing that the chapter before it just made, merge the two.
11. Put the create, find, view, and change of one thing into one chapter.
12. If a source splits work by operation, such as code by endpoint, still group by journey.
13. If a process has phases with their own actors, rules, or deadlines, give each phase its own chapter.
14. If a chapter grows past about fifteen steps, split it at a natural phase boundary.
15. For each branch, decide whether it is a divergent journey or a decision point (rules 2 to 4).
16. An event from another organization is a handover into a chapter. Put it into the chapter whose story it drives.
17. Make sure that each event is in exactly one named chapter. In an `.em.hcl` model, make sure that each workflow is in exactly one chapter.
18. Record each merge and each split as a decision (K8). Follow K9 for each unclear grouping.

Read `references/examples.md` when you need an example of chapters that are too small and their merge.

## Rules

1. A chapter describes a whole user journey. Do not make one chapter for an operation, a screen, or an endpoint.
2. A divergent journey gets its own chapter. The actor chooses before the process starts, and the screens and commands after that choice differ. Paying as a member and paying as a guest is an example.
3. A decision point stays inside its chapter. One trigger ends in one of several results, and the rest of the story stays the same. A card charge that succeeds or fails is an example.
4. To tell them apart, ask: "Does this branch start a different story, or does it only decide how this story ends?"
5. When in doubt, merge. One long journey is better than many small chapters.
6. No event and no workflow stays in an unnamed or general chapter.
7. A chapter changes no event and no story order.

## Result

The skill writes the chapters part: each chapter with its name and its members. In an `.em.hcl` model that is one `chapter` block with its `workflows` list for each journey. It writes decisions and open questions on the chapters (K8).

Report to the person: the chapters as one short list, each with one line about its journey, and each open question.

## Done when

1. Each event belongs to exactly one named chapter. In an `.em.hcl` model, each workflow is in exactly one chapter.
2. Each chapter name tells a journey from start to outcome, and no chapter is one operation, one form, or one or two steps.
3. Each decision point stays inside its chapter.
4. Each divergent journey has its own chapter.
5. Each merge and split has a decision, and each unclear choice is an open question.
6. No open request on the chapters part remains.
