---
layout: post
title: Getting engineers out of month-end
date: 2026-09-05
description: What I worked on at Checkr this summer, from a dashboard idea to driving month-end.
---

I interned at Checkr from June through August. The public version is on the
[home page](/): move monthly customer invoicing off engineer-in-the-loop batch
jobs onto Temporal, and give FinOps a way to run close without a production
console.

That sentence is the end of the summer, not the start. The first version of the
project was closer to a dashboard: watch the existing close, maybe wrap it. A
week of talking to the people who actually run invoicing made the scope honest.
If engineers were still going to sit in a room at month-end, a nicer status page
was not the work. The work was to drive the path, and to put the controls in
FinOps's hands.

The first architecture I was ready to defend mostly watched. Someone who owns
Temporal in production said the quiet part: if you take on durable execution,
the workflow should do something. A monitor that cannot recover is paying for
determinism and getting an audit log. We sat down, threw the first plan out, and
replaced it with one that kicks work, waits for humans, and fans out delivery. I
prototyped two directions in parallel instead of arguing for the leftover one.
Later feedback, which I deserved, was to treat those as iterations rather than
as a scorecard of which design was "wrong."

I also sat in on a real close, not just a design review. The pain was specific
without being exotic: files that did not match, rows that failed because data
was missing, a browser cache that looked like a permissions outage. None of that
belongs here as a play-by-play. It is why fail-closed and a list of failures
beat a count. A dry run later in the summer is what I trust more than the
diagrams. It completed. It also showed things a green test suite will not.

A few habits paid rent. Confirm the current data flow before you assume the
target architecture already shipped. Follow an in-repo pattern instead of
inventing a new flag. Split a migration from the logic that uses it. Keep diffs
small enough to review. A change can be mergeable and still wrong to land
during a live run. When two systems both think they own a transition, they
race; pick a driver.

I am not going to walk through the internals. Measure a topology against cost
and platform limits before you fall in love with it. Do not put operators on a
vendor UI they will not live in. Write down what is still unfinished so the
next person does not have to guess.

The interesting part was making the blast radius of a bad invoice smaller, and
replacing a count of failures with a list.
