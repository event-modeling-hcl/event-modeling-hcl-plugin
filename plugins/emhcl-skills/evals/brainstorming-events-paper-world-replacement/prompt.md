---
description: Business event discovery from screen-heavy replacement evidence without losing sources or system execution.
tags: [method, discovery, paper-world]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

We are replacing a lunch delivery application. The roles part already contains Customer and the system actor Dispatch Allocator. We are working only on the events part. Use the inline sources below; do not look for application files. Give the proposed event list, key facts, and supporting evidence in the reply. Do not write files or change any other model part.

Source SCREEN-17, screenshot and walkthrough recorded with the product owner on 4 November:
- Customer C-8 chooses meal M-2, quantity 2, delivery address "14 Oak Street", and delivery slot "12:00–12:30". The action is labelled "Save". The owner says this commits order O-104 for preparation and delivery; it is not a saved draft.
- The page then shows "Saved successfully", reloads its grid, and starts polling a status panel. The application log labels these steps "Order Row Inserted", "Grid Refreshed", and "Status Polled".
- The panel shows total meals ordered today, currently 47, and the latest assigned driver. The total changes as other customers order.

Source OPS-6, confirmed by the dispatcher on 5 November:
- After a committed order, Dispatch Allocator automatically chooses a driver from the available drivers and records that assignment against the order. For O-104 it assigned driver D-3. No dispatcher clicks an approval button or carries out this assignment.
- The business needs to retain which delivery address and slot the customer committed to and which driver was assigned. The product owner has not yet said what should happen when no driver is available.

The existing event list is: Order Row Inserted, Grid Refreshed, Status Polled, Driver Field Updated, Daily Meal Total Changed. Brainstorm the replacement list from these sources. Keep unresolved business behavior visible rather than guessing it.
