---
name: eventmodeling-cataloging-roles
description: Builds the catalog of human roles, system actors, and teams of an event model, each with what it can do and what it cannot do. Use it when someone asks who acts in a domain, asks to list the users, roles, staff, or outside systems, starts a new model, or names a new actor in the source material. Writes roles only. Does not write events, screens, commands, or the issuer of a command.
metadata:
  version: "1.0.0"
  contract: "K0 K8 K9 H0 H1 H10"
---

# Cataloging roles and actors

This skill tells who acts in the domain. It writes the roles part (K0): each human role, each system actor, and each team, with what it can do and what it cannot do. Every later part names its actors from this catalog.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs:

- The sources: requirements, notes, documents, answers from people.
- The roles part of the model, if it exists. Add only what is missing.
- The open requests on the roles part.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

## Procedure

1. Resolve each open request on your part first.
2. List each kind of person who does something in the domain. A human role is a kind of person with its own goals.
3. List each system that acts without a person. A system actor is a program that reacts to a time, an event, or a call.
4. List each team that the sources name as an owner of work.
5. Name each entry in business words. Use "Librarian", not "User Type 2".
6. If a source says only "user" or "admin", find the role it means. If no source tells it, follow K9.
7. For each human role, write one line about what the role does in the domain.
8. For each human role, list its key actions. A key action is a change that the role starts.
9. For each human role, list what it cannot do. Take the limits from the sources.
10. For each system actor, write whether it is inside this system or outside it.
11. For each system actor, write what makes it act and how it talks to this system in plain words, for example "sends a message when a payment clears".
12. If two roles have the same actions and the same limits, they can be one role. Follow K9 to decide.
13. If a role has no action and sees nothing, follow K9 to decide whether it belongs in the model.
14. Give each entry an evidence record under K8.
15. In an `.em.hcl` model, a system actor inside the system is a processor, and the roles part cannot write it. Report it in your result, and write a request (K8) concerning `processor` with its name, its trigger, and its contact.

Read `references/examples.md` when you need a full catalog to compare against.

## Rules

1. No entry has a generic name such as "User", "Admin", or "Customer Type".
2. Each human role has at least one key action and at least one limit. A limit that no source gives is an assumption (K8).
3. A system actor is an entry of the catalog. It is not a second story inside a chapter.
4. A new actor that a later part needs goes into the catalog before that part uses it.

## Result

The skill writes the roles part: one entry for each human role, system actor, and team, with its description, key actions, and limits. A system actor also has its place (inside or outside), its trigger, and its contact. It writes evidence, open questions, and assumptions on these entries (K8).

Report to the person: the catalog as a table, each assumption, and each open question.

## Done when

1. The model lists each human role and each system actor that the sources name.
2. No entry has a generic name such as "User" or "Admin".
3. Each human role has a description, at least one key action, and at least one limit.
4. Each system actor has its place, its trigger, and its contact, in the model or, for an internal actor in an `.em.hcl` model, in a request concerning `processor`.
5. Each entry has an evidence record with a certainty.
6. Each open point about an entry is an open question or an assumption on that entry.
7. No open request on the roles part remains.
