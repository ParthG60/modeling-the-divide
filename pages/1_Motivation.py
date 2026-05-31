"""Page 1 — Motivation: why I built this and the thesis it argues."""

from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Modeling the Divide", layout="centered", page_icon="⚖️")

ASSETS = Path(__file__).parent.parent / "assets"

st.title("Modeling the Divide")
st.markdown(
    "#### A small model of how a society splits into two, and why I think it has "
    "gotten worse since I built it."
)
st.caption("An interactive companion to my 2024 St Andrews dissertation. By Parth Goyal.")

st.markdown(
    """
In 2024 I wrote my undergraduate dissertation on a question I kept coming back to:
why does a population split into two hostile camps? Not ordinary disagreement, but a
society hardening into two sides that can barely talk to each other.

I want to be precise about what I mean, because this distinction is what the whole
model rests on:

> *"Variation in opinion is usually important for a democratic society, as the
> exchange of ideas and debate is important for truth seeking. However political
> polarization is not simply a variation of opinion."*

Polarization comes in two flavours, and I model both. The first is **ideological**:
the distribution of opinions becomes bimodal, so the middle hollows out and people
pile up at two extremes. The second is **affective**: the emotional gap. It isn't
just that we disagree, it's that we increasingly dislike and distrust the people
who disagree with us.

### Why it matters

I cared enough to spend a year on this because polarization isn't a spectator
sport. Here is the line from the dissertation that became the thesis of the whole
project:

> *"Political polarization undermines democratic processes by fostering an
> environment where compromise becomes increasingly difficult. It leads to a
> decline in the quality of governance, as policymakers prioritize party loyalty
> over the public good."*

I wrote that in 2024. Since then the trend has continued: deeper partisan hostility,
record-low trust in institutions, and incentives that reward party loyalty over
governing. The next page lays out the evidence so you can judge for yourself.

### What this is

This isn't a forecast or a proof. It's a deliberately simple model, a few hundred
agents on a left-to-right line with rules for who talks to whom and how they shift
afterwards, that reproduces the mechanism by which everyday interactions harden into
a societal divide. Two quotes I put at the front of the dissertation, and still
believe, set the right expectations:

> *"All models are wrong, but some are useful."* (George Box)
>
> *"Science is the art of systematic oversimplification."* (Karl Popper)

### How to read this

A short, signposted walkthrough. Use the sidebar to move through it:

1. **The Evidence**: what has happened to polarization and governance since 2024.
2. **The Model**: the starting setup, and why I made each assumption.
3. **What Happens**: run it forward, and the findings that surprised me.
4. **Playground**: your turn, move every dial and try to break it.

You don't need any maths to follow along. Start with **The Evidence** in the sidebar.
    """
)

pdf = ASSETS / "Goyal-2024-Modeling-the-Divide.pdf"
if pdf.exists():
    st.download_button(
        "Read the full dissertation (PDF)",
        data=pdf.read_bytes(),
        file_name="Goyal-2024-Modeling-the-Divide.pdf",
        mime="application/pdf",
    )

st.divider()
st.page_link("pages/2_The_Evidence.py", label="Next: The Evidence", icon="➡️")
