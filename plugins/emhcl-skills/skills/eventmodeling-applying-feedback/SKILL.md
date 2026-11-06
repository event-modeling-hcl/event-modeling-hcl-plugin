---
name: eventmodeling-applying-feedback
description: Turns free comments from reviewers on a prototype, on the model, or on a merge request into requests on the commented elements, each traced to one comment. Each clear comment becomes a request for a wording change, a field change along its chain, a rule as a scenario, or a new step. Ambiguous and opposite comments become questions with options. Use it when someone says "here is the feedback", pastes review comments, or asks to work merge request comments on the model into it. Does not write events, commands, screens, read models, scenarios, or any other model part. Does not handle answers to open questions of the model. Does not read code changes.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K2 K3 K8 K9 H0 H10"
---

# Applying feedback to the model

Reviewers try a prototype, read the model, or comment on a merge request. This skill turns each clear comment into a request on the commented element, concerning the part that must change, and a decision that records the comment. Ambiguous and opposite comments become questions. It writes records only, never an element of any model part.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs:

- the comments. The minimum input of a comment is its text and the element it is about, by name or by place.
- optional: a trail for each comment. A trail holds the events the person saw and their last interaction, such as a click or a submit.
- a merge request review comment anchored to a file and a line is a valid input. The anchored line names the element.
- the model: the commented elements, their slices, and the neighbor slices

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

## Procedure

1. Read each comment, its element, and its trail when one exists.
2. Find the element in the model. For a merge request comment, read the block at the anchored line. With a trail, start at the slice that the trail names. Otherwise search the screens, commands, and read models for the element name or the commented text.
3. Put the comments on one element together. Treat them as one change.
4. Apply the ambiguity test of K9 to each comment. If two comments on one element want opposite results, do not pick one. Ask in step 8.
5. Before you call a comment a wording problem, read the trail when one exists. If the person says "nothing happened", look for a missing event.
6. Classify each clear comment with the table under "Rules".
7. For each clear comment, write a decision with the comment and the reviewer as source. Then write one request (K8) on the element for each part that must change. Name the comment in the request.
8. Collect the ambiguous and opposite comments. Ask about all of them in one message (K9), with options.
9. Run the rule review under "Rules" on every slice that a request changes or adds.
10. Report under "Result".

## Rules

### From comment to part

| The comment is about | Request | Part that the request concerns |
| --- | --- | --- |
| wording, a label, a heading | change that text in place | the part of the element that holds the text |
| a missing or unwanted field | change the field along its whole chain (K2) | the part of each element along the chain |
| a rule, such as "only once" | add or change a scenario | command scenarios or read model scenarios |
| a new step, page, or decision | a new slice right after its predecessor | events, screens, commands, read models, and story order, as the step needs |
| ambiguous | none | a question to the person |

### A new step is a new slice

A reviewer often describes several steps as one flow. If a comment adds a step, request a new slice for it under K3, right after the slice it follows, not at the end. The commented slice keeps its one command. If a comment asks for a step and also a wording change, split it into two requests.

Before you request a slice, read the neighbor slices. If the step already exists, point to that slice.

### Options for an ambiguous comment

Build two or three concrete options under K9. With a trail, the events the person saw are the given, the last interaction is the when, and the expected result is the then. Without a trail, take the given from the scenarios of the element.

Read `references/examples.md` when you need options from a trail or a merge request comment.

### Rule review of the requests

Make sure that the requested changes keep these rules:

- One screen issues one command (K1).
- No command takes its fields from two screens.
- A total or other computed value is a read model field (K1).
- Each changed field keeps an origin (K2).
- No requested slice duplicates an existing slice.

If a rule fails, split or fix the request before you report.

## Result

The skill writes decisions, requests, and open questions. It writes no element. It does not rebuild a prototype.

The reply holds one line per comment: the comment in short, the element, and the parts that its requests concern. It names the new slices that the requests ask for. Then it holds the questions in one block. For a merge request comment, the line names the file and the line of the comment.

## Done when

1. Each request names exactly one comment, or one group of comments on one element.
2. Opposite and ambiguous comments are questions, with no request, and no clear comment became a question.
3. Each new step is a request for a new slice right after its predecessor.
4. Every requested change passes the rule review.
5. The reply has one line per comment.
