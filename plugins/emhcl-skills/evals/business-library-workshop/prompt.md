---
description: Exercise business library workshop.
tags: [business, acceptance, migration]
max_turns: 25
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Run a business-only Event Modeling workshop from these notes. A library member supplies member_id and copy_id at a checkout screen to Borrow Book. If the copy is available, the library records Book Borrowed with those two values. If it is already on loan, refuse the request with the stated reason 'Copy is already on loan'; do not record a failure event. Members can see which copies they currently have on loan from Book Borrowed and Book Returned facts. Start with the business timeline, then show the State Change and State View slices and observable scenarios. Keep the result in your reply: no HCL files, CLI commands, implementation design, or tooling installation.
