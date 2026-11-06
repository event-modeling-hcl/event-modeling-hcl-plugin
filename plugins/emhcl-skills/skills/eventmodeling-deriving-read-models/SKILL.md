---
name: eventmodeling-deriving-read-models
description: Derives one read model for each area of a screen that a person names as one thing, with fields traced to events, a natural query, a freshness tier, and a reason for each feeding event. It applies the split tests for wide fan-in. Use it when someone asks what data a page needs, where a displayed value comes from, or how to build a list or a dashboard from events. Does not write automation todo lists, screens, events, or scenarios.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K2 K4 K8 K9 H0 H3 H8 H10"
---


# Deriving read models

This skill gives each screen area the read model that it needs. An area is one part of a screen that a person names as one thing. After this skill, every screen has its data, and every read model field has a known origin. The skill writes the read models part only.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Read these parts of the model:

- screens: their displayed fields and the planned read models that they name
- events: every event and its fields
- streams: the identity of each event
- automations: to find automations without a todo list

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

## Procedure

1. Resolve each open request on your part first. Requests concerning read models often come from screens.
2. List every screen that shows data.
3. Find the areas of each screen. Most screens have one. Count two only when a person names two areas as different things. One list of one kind of item is one area.
4. Plan one read model for each area. Give every screen that shows prior state a read model.
5. A blank form for creating something needs no read model when it shows no prior state. Record the exemption as a decision (K8).
6. Take the fields from the displayed fields of the screen. Group them by the read model that they name.
7. Include only the fields that the screen shows.
8. For each field, name the event that sets it under K2. If the read model computes the value, the value starts here (K2). In an `.em.hcl` model, write a `field_source` with its inputs and a `description` of the rule.
9. If no event supplies a field, write a request (K8) on the nearest event, concerning events.
10. For each derived value, decide between an event and a read model field under K1. A derived value stays a read model field unless an event for it exists.
11. If a read model builds from more than three events, apply both split tests of K4. Record the reason for each field that keeps wide fan-in as a decision on that field.
12. Write the natural query of each read model in business words, such as "the open rentals of one rider".
13. Ask the freshness tier of each query under K9: instant, a few seconds, or minutes to hours.
14. Write one rationale note for each read model. For each feeding event, name the fields that it sets or changes, and why.
15. If an automation has no todo list, write a request on its processor, concerning automations.
16. If a screen field names a read model by a different field name, write the origin under K2.

## Rules

1. One read model serves one area. A screen-wide read model that pulls unrelated events together is a fault.
2. A wide fan-in reason belongs to one field, never to the whole read model.
3. When a later change adds an event to a read model, extend its rationale note. Do not write a second note.
4. A todo list of an automation belongs to the automations part, not here.
5. In an `.em.hcl` model, put the read model in the `state_view` workflow of its screen. If no workflow holds it, create a `state_view` workflow (H3). Write the natural query as `question` and the rationale note as `description`.

## Result

This skill writes read models, their fields, natural queries, freshness tiers, and rationale notes, plus their records (K8). It reports to the person each read model with its query, its feeding events, the split decisions, and the requests it wrote.

Read `references/examples.md` for a worked split of one screen into two read models.

## Done when

1. Every screen that shows prior state has a read model for each of its areas, and every exempt screen has a written reason.
2. Every read model field comes from an event under K2, or is a computed value that starts here with its rule.
3. Every read model has a natural query and a freshness tier.
4. Every field that keeps wide fan-in has a decision with its reason.
5. Every derived value is a read model field, unless an event for it exists.
6. Every read model has one rationale note that covers each feeding event.
7. Every automation without a todo list has a request concerning automations.
8. Each open request on the read models part is resolved.
