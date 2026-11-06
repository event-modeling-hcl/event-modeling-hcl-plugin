---
name: eventmodeling-facilitating-workshop
description: Plans and guides a live event modeling workshop with a group of people. It builds the session plan with a time box for each model part in gate order, covers participants, pacing, quiet and dominant people, disagreement, the remote format, and writes the follow-up summary. Use it when someone asks to prepare, run, or follow up an event modeling workshop or session with a team, a product owner, or domain experts. Writes nothing in the model. Does not build a model alone without a group.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K8 K9 K11 K12 H0"
---

# Facilitating a workshop

A facilitator guides a group of people through the parts of a model and keeps time. This skill plans the session in the order of the gates of K12, handles people and disagreement, and writes the follow-up summary. It writes nothing in the model. During the session, the skill whose description writes a part writes that part from the statements of the group.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Get these inputs: the domain, the goal of the workshop, the participants and their roles, the date, the length, the format (room or remote), and the model if one exists.

If the model is an `.em.hcl` file or folder, read it under H0 and change nothing in it yourself.

For invitations, the room, the materials, the remote setup, a plan over several days, and a repair session, read `references/logistics.md`.

## Participants

Plan for five to eight people. A smaller group misses views. A larger group is hard to guide.

- Required: a product owner or a domain expert, two or three developers, one or two testers, and one facilitator.
- Optional: a user experience designer, a security lead, an operations person, and a real user.

One person cannot speak for all roles. If a required role is missing, propose to move the session.

## Procedure

1. Find the first gate of K12 that fails in the model. With no model, start at roles. The session starts at that part.
2. Build the session plan: one row for each part from that gate on, in the order of K12, with its time box from the table below. Add a break at least every 60 minutes, or every 30 minutes in a remote session.
3. Prepare the questions for the parts that exist under K11. Walk them in story order.
4. Send the invitation. Use `references/logistics.md`.
5. Run each part with the steps below.
6. At the end, write the follow-up summary. Use the follow-up section below.

## Time boxes

The times are starting values. Adjust them to the size of the domain and the speed of the group.

| Part (K12 order) | Time box |
| --- | --- |
| roles | 10 minutes |
| events | 15 to 25 minutes |
| chapters and story order | 15 minutes for each chapter |
| screens | 5 to 7 minutes for each screen |
| streams | 10 minutes |
| lifecycles | 10 minutes for each stream |
| commands | 20 minutes |
| automations | 10 minutes for each automation |
| external mappings | 10 minutes for each external event |
| read models | 15 minutes |
| command scenarios | 10 to 20 minutes for each command |
| read model scenarios | 5 to 10 minutes for each read model |
| reviews | 20 to 30 minutes for the question tour |
| slice status | 10 minutes |
| ownership | 15 minutes |
| chapter summaries | After the session, in the follow-up |

## Each part of the session

1. Say the goal of the part in one sentence: its gate in K12.
2. Let people call out ideas first. Capture each idea without a filter.
3. Give the ideas to the skill whose description writes that part. That skill applies its rules and writes the part and its records.
4. Read each result aloud in business words (K11) and ask the group if it is right.
5. Each open item becomes an open question in the model, written by the writer of that part.
6. When the time box ends, move on. The open items of the part stay open questions.

In the events part, let the group name events freely first. Filter them afterward. In the scenario parts, give each role its own lens. The domain expert judges the business behavior. The developer judges whether the team can build it. The tester judges whether the team can test it.

## Paper-world reset

If people describe controls instead of work, use the offline-first reset in K1. Also use it for unclear handoffs or conflicting terms. Keep the exercise inside the current part's time box.

1. Ask one participant to walk one real case with people, paper, and pens.
2. Start with who requests the action and what starts the request.
3. Ask who receives the paper and what they read before acting.
4. Walk the supplied eligibility rules and both the allowed and refused outcomes inside this exercise.
5. Ask what each outcome records and what passes to the next actor.
6. Ask another participant to describe a correction, a delay, or a disputed decision in that case.
7. Read the account back and ask which statements are confirmed.
8. Give the answers and their sources to the writer of the affected part.

If the exercise exposes work in another part, send it to that part's writer. Keep unresolved decisions as open questions under K8. Resume the current part without adding another gate or writing a separate paper model.

## Pacing

Spend five to seven minutes on one item. Take a break of ten minutes every 45 to 60 minutes. Watch for these signs: phones, one long speaker, long silence, or tired faces. Then take a break, change the activity, or show what is done and what is left.

## People

- A quiet person: ask the person by name, in a friendly way.
- A dominant person: thank the person and ask the others.
- A skeptic: ask for the concern and take it seriously. It often shows a real problem.
- An idea generator: capture each idea and sort the ideas later.

## Disagreement

1. If one answer is clearly right, use it.
2. If reasonable people disagree, record one open question with both views as options (K9) and move on.
3. If the question does not matter now, record it as an open question for the build team.
4. Never stay on one item past its time box.

## Remote format

1. Keep each session to 90 minutes.
2. Take ten minutes of break every 30 minutes.
3. Let everyone add ideas in silence before the talk.
4. Give one person the drawing and one person the notes.
5. Record the session for people who cannot join, if the group agrees.
6. Give time for written feedback after the session.

## Follow-up

On the same day, make sure that each result of the session is in the model. Within two days, send the follow-up summary with these parts:

- each participant and the role that the person spoke for,
- each decision and its reason,
- each open question, with the element that it is on,
- the first gate of K12 that still fails, as the start of the next session,
- each next step with a person and a date,
- a request for corrections and missed items.

Late answers go to the skill whose description applies answers to open questions.

Read `references/examples.md` when you need a worked session plan and summary.

## Result

This skill writes nothing in the model. It gives the facilitator a session plan before the session and a follow-up summary after it.

## Done when

1. The session plan lists the parts of K12 in gate order from the first failing gate, with a time box for each part and a break at least every 60 minutes, or every 30 minutes for a remote session.
2. The session plan lists the participants by role and states that each required role is present, or it proposes to move the session.
3. Each decision of the session is in the follow-up summary with its reason.
4. Each open item of the session is an open question in the model.
5. The follow-up summary lists each participant, each open question, the first failing gate, and each next step with a person and a date.
