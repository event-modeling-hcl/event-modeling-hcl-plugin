---
name: eventmodeling-measuring-scenario-coverage
description: Measures how much of the business logic of each slice its scenarios cover, as a percentage, and lists up to 10 missing scenarios for each slice, most important first. Use it when someone asks how well the scenarios cover a chapter or the whole model, which test cases are missing, or which scenarios to write next. Writes nothing in the model. Does not write scenarios.
metadata:
  version: "1.0.0"
  contract: "K0 K5 K6 K9 K10 H0 H9"
---

# Measuring scenario coverage

This skill gives a coverage percentage for each slice and a short list of the meaningful scenarios that are still missing. Coverage is the share of meaningful cases that existing scenarios already state. The number guides what to model next, so it must be honest. The skill writes nothing in the model.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs:

- the chapter that the person names, or every chapter when the person names none
- for each slice: its command, read model, or automation, the fields, the connected events, and the scenarios

If a name fits more than one chapter, ask under K9. If the model is an `.em.hcl` file or folder, read scenarios and their `case` values as H9 describes.

## Procedure

1. Take one slice.
2. Derive its cases from K5. For an automation slice, include its issued command, processor dispatch, and pending-work view. These are distinct behaviors of one slice.
3. Keep meaningful business cases under K5. Generic technical tests do not count. A repeated delivery that prevents a second business fact can be meaningful.
4. Take each existing scenario. Match it to the case whose given, when, and then it states exactly. A `case` value on a scenario is a hint, not proof. Read the steps.
5. Do not count repeated scenarios, generic technical tests, or impossible process cases. Preserve supplied acceptance behavior even when it does not count toward this measure.
6. Compute the coverage: 100 times covered cases divided by meaningful cases. Round down to a whole number.
7. A pass-through slice reaches 100 only when its scenarios cover every supported meaningful case. One happy path does not cover a supplied duplicate or correlation rule.
8. If you cannot derive any meaningful case for a slice, give no value. Say why.
9. List the uncovered cases as missing scenarios. Give each one a short title.
10. Add a given, a when, and a then to each missing scenario when the model lets you state them. Write one short sentence each, in the words of the model.
11. Use concrete values only when the model holds them (K6). Leave a part out rather than guess it.
12. Keep at most 10 missing scenarios for each slice. Put the most important first.
13. Repeat for every slice in scope.
14. Write the report.

## Rules

1. Only meaningful cases count, for existing scenarios and for missing ones.
2. Do not invent a case to make the list longer.
3. A slice with no meaningful case gets no value, not zero.
4. Every percentage in the report rounds down to a whole number. Two of three is 66, not 67.
5. Importance follows business impact. The happy path comes first. Rejections that protect money, safety, or rights come next.
6. Do not store the coverage in the model.

## Result

This skill writes nothing in the model.

It reports to the person one table. Each line holds the slice, its coverage, and its missing scenarios. Under the table, one line gives how many slices have a value, the average coverage of those slices (rounded down), and the three slices with the lowest coverage.

Read `references/examples.md` when you need a sample report.

## Done when

1. Every slice in scope has a coverage value or a stated reason for no value.
2. Every value equals 100 times covered divided by meaningful, rounded down.
3. Generic technical tests count neither as covered nor as missing business cases. Supplied repeat, translation, and external-failure outcomes count when meaningful under K5.
4. Each slice lists at most 10 missing scenarios, most important first.
5. Each missing scenario uses the words of the model and no guessed value.
6. The report gives the average and the three lowest slices.
7. The model is unchanged.
