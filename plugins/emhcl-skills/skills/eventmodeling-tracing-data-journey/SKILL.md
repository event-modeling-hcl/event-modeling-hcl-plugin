---
name: eventmodeling-tracing-data-journey
description: Follows one piece of information through the model, from where it enters to where it leaves, and shows each stop in a table. Each stop has one role (origin, stored, transformed, used, or sent) and the field name that the information has there. Use it when someone asks where one value comes from, where the model uses it, which events store it, or where personal data such as a phone number goes. Does not explain a whole flow step by step, and does not audit the origin of every field in the model. Writes nothing.
metadata:
  version: "1.0.0"
  contract: "K0 K2 K9 K10 H0 H8"
---

# Tracing the journey of one piece of data

This skill answers one question: where does this piece of information come from, and where does it go? The person gets a table with one stop for each element that carries the information, in flow order. The skill writes nothing. Gaps in the journey become findings in the reply, not invented stops.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

You read these parts of the model:

- The elements of each chapter and their fields.
- The declared origin of each field (K2): the stated upstream source of a renamed or derived field.
- The scenarios and the descriptions of the elements on the journey.
- The personal data mark on each field, if the model has one.

If the model is an `.em.hcl` file or folder, the declared origins follow H8, and a personal data field has `pii = true`.

## Procedure

### Choose the subject

1. Take the subject from the message of the person: one piece of information, for example "rider phone number". If the person selected one field, use that field.
2. If no subject is given, or several pieces of information fit equally well, ask (K9). Offer the field names that you found as options.
3. If the subject holds two pieces of information, trace the first one. Offer the second one as a new trace.

### Find every carrier

4. Search the element names and the fields of each chapter for the subject and its obvious variants: other spellings, short forms, and the language of the model.
5. Collect each field with the same name, and each field with a prefix or a new name for the same information.
6. Follow the declared origins from each field that you have, both upstream and downstream, until no new field appears.
7. Trace a rename only through a declared origin. Do not guess a rename from similar names.
8. Treat a field that only sounds similar as different information. Leave it out, or name it in the note of the stop where it sits.

### Order the stops

9. Arrange the stops from the first input to the final consumer. Follow the usual path: screen, command, event, read model, screen. Also follow event, automation, command.
10. After an event that stores the information, list the read models that it feeds, then the automations.

### Give each stop a role

11. Give each element one role from the table below. Show each element once. If two roles fit, choose the role that tells the most about the element.
12. If a command takes the field from its screen, the command is used. If that screen is not in the model, the command is the origin.

| Role | The element |
| --- | --- |
| origin | introduces the information into the system: a form input, an outside event, or an import. Information with several entry paths has several origins. |
| stored | is an event that records the information. Each event that carries the field is a stop. |
| transformed | changes the information: a rename through a declared origin, a derived value, or a normalization that a description or a scenario states. |
| used | reads the information: a command that passes it on or tests it, a read model or a screen that shows it, or a scenario that decides on it. |
| sent | gives the information to a party outside the system, such as an automation that calls a mail or payment service. |

### Describe each stop and the gaps

13. Give each stop the element name as the model writes it, the field name on that element, the name of the slice that holds it, and a note of a few business words. For a transformed stop, say what changes. For a used stop, say how the element uses it.
14. Use no identifiers in the table.
15. If a screen shows the information but no read model carries it there, report a gap.
16. If an event stores the information but no element reads it, report a gap.
17. Do not add a stop to close a gap. Write each gap as a finding in the summary, with the element and what is missing (K10).

Read `references/examples.md` when you need a full example of the result.

## Rules

1. One trace follows one piece of information.
2. Only declared origins link two stops. Similar names never do.
3. Each element appears once, with one role.
4. A gap is a finding. It never becomes an invented stop.

## Result

The skill writes nothing in the model. If the person asks for a gap to be fixed, the fix goes to the writer of that part through a request on the element (K0).

It reports three parts:

1. One line that names the subject, where it starts, and how many stops each role has, for example "Rider phone number: starts in 1 place, stored in 2 events, used in 3 places, sent in 1 place."
2. A summary of 1 to 3 sentences. Name personal data and each gap here.
3. A table with the headings Role, Element, Field, Slice, and Note, with one line for each stop in flow order.

## Done when

1. Each stop joins the journey through a declared origin or the same field name, never through a similar name, and fields that only sound similar are not stops.
2. Each stop has one role, the local field name, its slice, and a short note.
3. The trace has one subject, or the person chose it after a question.
4. The summary names personal data when a field on the journey is marked as personal data.
5. Each gap is a finding in the summary, and no stop is invented.
6. The model is unchanged.
