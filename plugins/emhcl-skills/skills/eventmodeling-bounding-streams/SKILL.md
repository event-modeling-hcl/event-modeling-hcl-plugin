---
name: eventmodeling-bounding-streams
description: Gives each event stream one business identity and fixes streams that hide a collection, a log, or two identities. Use it when someone asks which aggregate or stream an event belongs to, what the consistency boundary of a thing is, or why a stream keeps growing. Writes streams only. Does not write lifecycle states or moves, events, or read models.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K8 K9 H0 H5 H10"
---

# Bounding event streams

This skill gives each event stream one business identity. It writes the streams part (K0): each stream, its identity, and the stream of each event. An event stream is the ordered history of one business thing.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs:

- The events part and the facts each event carries.
- The chapters and the story order, when they exist. In an `.em.hcl` model, they exist only after the slices (H3), so read the events and their facts instead.
- The streams part, if it exists.
- The open requests on the streams part.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

## Procedure

1. Resolve each open request on your part first.
2. For each stream, ask the golden question: "This stream is the history of exactly which one thing?"
3. Write the answer as one identity, such as the booking number of one booking. Never write a category, such as "bookings".
4. If no single identity answers the question, the stream is a collection or a log. Go to step 8.
5. Put each event next to the identity. Ask: "Did this event happen to this one thing?"
6. If every event passes, keep the stream, even when its history is very long.
7. If some events fail, find the thing that each failing event really happened to. Give it its own stream.
8. If the stream holds "all of X", it is a collection. Remove it. Write a request (K8) concerning the read models part, with the question that the collection served.
9. If the stream mixes unrelated concerns, it is a log. Make one stream for each concern, each with its own identity.
10. If one identity turns out to be two, split the stream. Give each part the identity of its own lifecycle.
11. If a child thing starts and ends with its parent, keep it in the parent stream. This is a composite stream.
12. If the stream holds the active life of a thing and its long-term record, split them only when the two have different users, rules, or retention. Record the reason as a decision (K8).
13. If one business change is spread over several events, or one event holds several changes, write a request (K8) concerning `event`.
14. If an event lacks the identity field of its stream, write a request (K8) concerning `event`. If the identity type does not exist, write a request concerning `field_type`.
15. Record each split, merge, and removed stream as a decision (K8). Follow K9 when the identity of a thing is unclear.

Read `references/examples.md` when you need worked cases from libraries, banks, or subscription services.

## Rules

1. A stream has exactly one business identity. A category name is never an identity.
2. Length alone is never a finding. A savings account open for forty years is one correct stream.
3. A stream that grows without a natural end is a warning sign. Its identity probably covers a whole population.
4. A stream that cannot answer "What is the state of this thing?" is not a thing.
5. A composite stream has few, bounded children that share the lifetime of the parent. A child with its own lifecycle gets its own stream.
6. The fix for a wrong boundary is a narrower or different identity, never a technical workaround.

## Result

The skill writes the streams part. In an `.em.hcl` model that is the `aggregate` blocks with their `identity`, and the `aggregate` attribute on each event (H5). It writes decisions and requests (K8).

Report to the person: one row for each stream with its thing, its identity, and its events, each removed stream and where its events went, and each request.

## Done when

1. Each stream has one named business identity, never a category.
2. Each event belongs to exactly one stream, and it happened to the thing that the identity names.
3. No stream is a collection. Each removed collection has a request on the read models part.
4. No stream is a log of unrelated concerns.
5. No finding rests only on the length of a stream.
6. Each split between active life and long-term record has a decision with its reason.
7. No open request on the streams part remains.
