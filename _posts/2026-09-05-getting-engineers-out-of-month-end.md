---
layout: post
title: Getting engineers out of month-end
date: 2026-09-05
description: What I worked on at Checkr this summer.
---

I interned at Checkr from June through August. The public version is on the
[home page](/): move monthly customer invoicing off engineer-in-the-loop batch
jobs onto Temporal, and give FinOps a way to run close without a production
console.

I am not going to walk through the internals. What is worth keeping, for me, is
the shape of the work. A money path is unforgiving. Fail closed when a status is
unknown. Measure a design against cost and limits before you fall in love with
it. A dry run will show you failure modes that a green test suite will not. Write
down what is still unfinished so the next person does not have to guess.

The interesting part was making the blast radius of a bad invoice smaller, and
replacing a count of failures with a list.
