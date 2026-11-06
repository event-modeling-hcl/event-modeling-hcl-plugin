---
name: eventmodeling-writing-chapter-summary
description: Writes the one summary of each complete chapter, with an overview of the whole source in the first chapter. The summary holds the scope, dates, rules, requirements, data, elements, open questions, assumptions, the items left out of the model, and the design reasons. Use it when someone asks to summarize a finished chapter, to write the chapter overview for a tender or a specification, or to update the summary after the chapter changed. Does not explain one flow step by step, and does not write decisions, assumptions, or any element. Writes chapter summaries only.
metadata:
  version: "1.0.0"
  contract: "K0 K8 K9 H0 H10 H11"
---

# Writing a chapter summary

This skill writes the one summary that each chapter keeps. The summary tells a reader who never saw the source what the chapter covers and why it has its shape. It holds enough detail to start specifying and building the chapter. The skill writes one part: chapter summaries.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

The chapter must be complete: its elements, scenarios, and slices exist, and no open request remains on them. Each review finding is fixed or recorded as accepted debt. The summary describes the finished shape, not a plan.

You read these inputs:

- The elements, slices, and scenarios of the chapter.
- The records of the chapter (K8): open questions, assumptions, decisions, accepted debt, evidence sources, and evidence.
- The decisions for items that a source holds and the model leaves out. They give the "Not modeled" section.
- The ownership of the elements, when it exists.
- The source documents that the evidence sources name, for each number, date, and threshold.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`. The summary is the `description` of the `chapter`, as a multi-line string (H11). Write no file beside the model.

## Procedure

### Prepare

1. Resolve each open request on your part first. Your part is the summary of each chapter.
2. Make sure that the chapter is complete. If a part is missing, stop and name the missing part.
3. Read the existing summary of the chapter. If one exists, update it in place and change only the sections that the chapter changes affect.
4. Write in the language of the source document. If no source document exists, use the language of the model.

### Write the chapter sections

5. Write the sections in the order of the table below. Name each element with its exact name in the model.
6. Use a table when a section lists items with several parts. If a section has no content, write "None" under it. Never drop a section.
7. If the chapter is simple, say so in a few lines. Do not pad the summary.
8. Take each fact from the model or the source. General domain knowledge can appear only as a risk or a question.
9. Copy each number, date, and threshold from its source word for word (K8), with its source reference.
10. Refer to each open question by its subject. Do not copy its full text.

| Section | Content |
| --- | --- |
| What this chapter covers | 2 to 5 lines. The phase of the process, who acts, what starts the chapter, and what ends it. The main entities and their identity keys. |
| Dates and deadlines | A table with what, when, source, and the effect of a missed date. |
| Business rules | A table with the rule and its exact thresholds, the element that holds it, the scenario, and the source. Name the rules that are scenarios with an error instead of events. |
| Requirements and deliverables | Mandatory and optional items, each with the element that tracks it. |
| Data and documents | The forms and documents that the parties exchange, with their known fields. |
| Elements | The counts and the names of the events, commands, read models, automations, and screens. The slices by kind. The external parties and their translated events. The review result. |
| Read model reasons | Why each read model has its fields. Where one read model serves two places. The recorded reason for each read model with wide fan-in. |
| Integration gaps | Gaps between chapters or with other systems, each with the possible resolutions and the matching open question. |
| Corrections | Changes to order or design during modeling, and the reason for each, from the decisions. |
| Open questions and risks | A table with the question or risk, its sources, and why it matters. Include contradictions, missing information, one-sided clauses, and unrealistic dates. |
| Assumptions | Each assumption that the chapter depends on, one line each, with its reason. |
| Not modeled | Source content in the scope of the chapter that the model leaves out, each with its reason. |

One-sided clauses are terms that favor one party, for example on liability, penalties, intellectual property, or payment.

### Write the overview in the first chapter

11. If the chapter is the first chapter in story order, put the overview above its sections, in the order of the table below.
12. Put content that spans chapters into the overview once. In each other chapter, refer to the overview for it.

| Overview section | Content |
| --- | --- |
| Title and source | The title of the source, its files and page counts, and the perspective. The perspective is whose view the model takes, stated as an assumption. |
| At a glance | 5 to 8 lines. What the source is, who takes part, what it asks for, its value or scope, and the three points that matter most. |
| Go and no-go criteria | The conditions that allow or exclude a party, and the mandatory proofs, each with its exact threshold and source. "None" when the source sets none. |
| Evaluation | A table with the criteria, their weights, the scoring method, and how price counts. |
| Dates for the whole document | Dates that apply to more than one chapter. |
| Chapters | A table with each chapter, its purpose, and its key elements. |
| Implementation notes | A suggested build order from the event dependencies between slices, and a first thin slice to build. |

### Finish

13. Write the summary on its chapter. Make sure that each chapter has exactly one summary.
14. If the summary shows a gap in another part, write a request (K8) on the element, concerning that part.

Read `references/examples.md` when you need a full example of a first-chapter summary.

## Rules

1. Each chapter has exactly one summary. A new run updates it in place.
2. The summary comes after the chapter is complete.
3. Content that spans chapters appears once, in the overview of the first chapter.
4. The summary holds no decision log. It refers to the decisions in the model.

## Result

The skill writes the summary of each complete chapter, and requests for gaps in other parts. It changes no element and no other record.

It reports to the person which chapters got a new or updated summary, and each request that it wrote.

## Done when

1. Each summary has every section in the table order, and an empty section says "None".
2. Each number, date, and threshold matches its source word for word and names its source.
3. Each complete chapter has exactly one summary, written after the chapter was complete.
4. The first chapter opens with the overview, and content that spans chapters appears only there.
5. Each open question and each assumption of the chapter appears in the summary.
6. Each "Not modeled" item has a reason.
7. A second run changed the existing summary and did not add a new one.
8. No file exists beside the model for the summary.
