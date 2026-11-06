---
name: eventmodeling-storyboarding-screens
description: Adds one screen for each state where a person looks at the state and decides, told from one actor at a time along the story of a chapter. Each screen lists the fields that it shows, the fields that it asks for, and the action that it offers. Use it when someone asks what a person sees or does at a step, asks to sketch the pages or forms of a process, or asks which screens a role needs. Does not write commands, read models, automations, or events.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K2 K6 K8 K9 H0 H3 H4 H8 H10"
---


# Storyboarding screens

This skill shows what people see and do along the story of a chapter. It gives one screen for each state where a person reads the state and decides. The story follows one actor until the work passes to another actor. The skill writes the screens part only.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Read these parts of the model:

- roles: the human roles and what each one can do
- events, story order, and chapters: the steps of the chapter in order
- screens: the screens that the model already holds. Reuse a screen when it shows the same state.
- read models: the read models that exist, as sources for displayed fields

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

## Procedure

1. Resolve each open request on your part first.
2. Walk the story of the chapter from its first step.
3. At each step, ask: "Does a person look at the state here and decide what to do next?"
4. If yes, add one screen for that state. If no person acts at the step, add no screen.
5. Give the screen to one human role from the roles part.
6. Before each screen, identify the role that acts next. Keep that actor until a real handoff makes the work wait on another actor.
7. Do not switch actors only because another role can also see a change.
8. Describe what the screen shows and what it asks for, in plain words. Do not design its look.
9. List each field that the screen shows. Name the read model that supplies it under K2. If that read model does not exist, name the planned read model and write a request (K8) on the screen, concerning read models.
10. List each field that the person enters. Its origin is the screen: it starts here (K2). Give it an example value under K6.
11. Name the one action that the screen offers. A page with several actions is several screens.
12. For each step after the screen, ask what the person sees next. Add that next state as a screen when a person decides there.
13. At each decision point, add the screen that the person sees on each path that needs a choice.
14. For each rejection that the person sees, describe what the screen says and what the person can do next.
15. If a displayed value has no clear source, write an open question (K8) on the screen.
16. Make sure that each human role has at least one screen. If a role has no screen, ask the person under K9 whether screens are missing or the role does not belong in this chapter.

## Rules

1. One screen for each state where a person decides. A change that nobody looks at needs no screen.
2. Each screen belongs to exactly one human role.
3. Each screen offers at most one action. A screen that only shows data offers none.
4. A step that runs with no person gets no screen. Leave it to the automations part.
5. This skill describes content, never layout, colors, or controls.
6. In an `.em.hcl` model, an entered field gets no `generated` and no `field_source`. The screen is its origin.
7. A screen with several areas stays one screen here. The read models part splits its data.
8. In an `.em.hcl` model, the screen that offers an action creates the `state_change` workflow of that action, named for the action. A screen that only shows data creates a `state_view` workflow. Leave the command and the read model out of the workflow.

## Result

This skill writes screens and their fields, plus their records (K8). In an `.em.hcl` model it also writes the workflow that holds each new screen, and requests on new workflows for the chapter and the board (H3). It reports to the person:

- the screens by role, in story order, with each handoff
- the planned read models that are still missing
- the roles that have no screen

Read `references/examples.md` for a worked set of screens with a handoff and planned read models.

## Done when

1. Each state in the chapter where a person decides has exactly one screen, and that screen belongs to one human role.
2. Each displayed field names an existing read model, or a planned read model with a request on the screen.
3. Each entered field has the screen as its origin (K2), with an example value.
4. Each screen offers at most one action, and the action is named.
5. Each rejection that a person sees has a described message and a next step.
6. Each human role has at least one screen, or an open question explains why not.
7. No screen stands for a step that runs with no person.
8. Each open request on the screens part is resolved.
