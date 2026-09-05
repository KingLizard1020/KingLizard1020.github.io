---
layout: post
title: Getting engineers out of month-end
date: 2026-09-05
description: What I worked on at Checkr this summer, and what still was not done when I left.
---

I interned on Checkr's monetization team from June through August. The job was monthly customer invoicing: tax, ERP, tie-out, then email. Until this summer that took a room of engineers on standby and a production console. The project was to get engineers out of it and put the controls in FinOps's hands.

The old path was a Sidekiq batch over tens of thousands of invoices. One bad row blocked everything behind it in a few-thousand-invoice batch, and a failure gave you a count, not a list. Recovery was someone typing into a Rails console during close. The replacement is Temporal: a monthly parent that waits for FinOps, then one durable workflow per invoice whose ID is the idempotency key. A bad invoice is now that invoice.

The shape of the system was not the first design. Temporal bills by Action, and a per-invoice poll at a tight interval was on the order of two hundred times the baseline cost. Event-pushed signals were about twice baseline. That number is what made a full Temporal path defensible. Child workflows were out too: they write into the parent history, and at this volume you blow the event cap. So the parent spawns independent siblings and does not get cancel-for-free. Pause and cancel had to be explicit.

A production-snapshot dry run of about 16% of a period is what I trust more than the design docs. It completed, and it also surfaced silent failures: an upload that reported success while invoices stayed parked, a heartbeat that never fired because the activity was too *slow* to reach the next count, a worker sized from an average that understated peak memory by half. On a money path the rule I kept coming back to was fail closed. Unknown Oracle status does not become success. A missing gate does not become "approved."

At handoff the engine was architecturally better and operationally behind. It had not replaced the old close. Duplicate prevention was still application-level. Some of the parent accounting from that dry run was not recoverable. I wrote that down on purpose. The interesting work was not the merge count. It was making the failure mode smaller, and leaving the next person a list instead of a story.
