"""Page 1 — Motivation: why I built this and the thesis it argues."""

import streamlit as st

st.set_page_config(page_title="Modeling the Divide", layout="centered", page_icon="⚖️")

st.title("Modeling the Divide")
st.markdown(
    "#### A small model of how a society splits into two — and why I think it's "
    "gotten worse since I built it."
)
st.caption("An interactive companion to my 2024 St Andrews dissertation · Parth Goyal")

st.markdown(
    """
In 2024 I wrote my undergraduate dissertation on a question that wouldn't leave
me alone: **why does a population split into two hostile camps?** Not drift, not
healthy disagreement — the hardening of a society into two sides that can barely
talk to each other.

I want to be precise about what I mean, because this is the distinction the whole
model rests on:

> *"Variation in opinion is usually important for a democratic society, as the
> exchange of ideas and debate is important for truth seeking — however political
> polarization is **not** simply a variation of opinion."*

Polarization comes in two flavours, and I model both:

- **Ideological** — the distribution of opinions becomes *bimodal*: the middle
  hollows out and the mass piles up at two extremes.
- **Affective** — the emotional gap. It's not just that we disagree; it's that we
  increasingly dislike and distrust the people who disagree with us.

### Why it matters

The reason I cared enough to spend a year on this is that polarization isn't a
spectator sport. In the dissertation I argued:

> *"Political polarization undermines democratic processes by fostering an
> environment where compromise becomes increasingly difficult. **It leads to a
> decline in the quality of governance, as policymakers prioritize party loyalty
> over the public good.**"*

That sentence is the thesis of this whole project. And here's the thing — I wrote
it in **2024**. Since then I think the prediction has aged uncomfortably well:
deeper partisan hostility, record-low trust in institutions, and politics that
rewards pandering to your own side over actually governing. The next page lays out
the evidence so you can judge for yourself.

### What this is

This isn't a forecast or a proof. It's a deliberately simple model — a few hundred
agents on a left–right line, with rules for who talks to whom and how they shift
afterwards — that reproduces the *mechanism* by which individual interactions
harden into a societal divide. Two quotes I put at the front of the dissertation,
and still believe, set the right expectations:

> *"All models are wrong, but some are useful."* — George Box
>
> *"Science is the art of systematic oversimplification."* — Karl Popper

### How to read this

A short, signposted walkthrough — use the sidebar to move through it:

1. **The Evidence** — what's happened to polarization and governance since 2024.
2. **The Model** — the starting setup, and *why* I made each assumption.
3. **What Happens** — run it forward, and the two findings that surprised me most.
4. **Playground** — your turn: move every dial and try to break it.
5. **Methodology** — the equations and exact rules, for the curious.

*You don't need any maths to follow the first four. Start with **The Evidence** in
the sidebar.* →
    """
)
