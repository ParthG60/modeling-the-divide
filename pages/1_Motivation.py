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
In 2024 I wrote my undergraduate dissertation on a simple question: why does a
population split into two hostile camps? I don't mean ordinary disagreement. I mean
a society hardening into two sides that can barely talk to each other.

The distinction matters, and the dissertation drew it clearly:

> *"Variation in opinion is usually important for a democratic society, as the
> exchange of ideas and debate is important for truth seeking. However political
> polarization is not simply a variation of opinion."*

I model two kinds. **Ideological** polarization is when the distribution of opinions
becomes bimodal: the middle empties and people cluster at the extremes. **Affective**
polarization is the emotional gap, where we not only disagree but dislike and
distrust the other side.

### Why it matters

Polarization degrades how a country is governed. The dissertation put it this way:

> *"Political polarization undermines democratic processes by fostering an
> environment where compromise becomes increasingly difficult. It leads to a
> decline in the quality of governance, as policymakers prioritize party loyalty
> over the public good."*

That was written in 2024. Since then the trend has continued: deeper partisan
hostility, record-low trust in institutions, and incentives that reward party
loyalty over governing. The next page shows the evidence.

### What this is

A deliberately simple model: a few hundred agents on a left-to-right line, with
rules for who talks to whom and how they shift afterwards. It reproduces the
mechanism by which everyday interactions harden into a divide. It is not a forecast
or a proof. Two quotes I kept at the front of the dissertation set the right
expectations:

> *"All models are wrong, but some are useful."* (George Box)
>
> *"Science is the art of systematic oversimplification."* (Karl Popper)

### How to read this

A short walkthrough. Use the sidebar or the Next links at the foot of each page:

1. **The Evidence**: what has happened to polarization and governance since 2024.
2. **The Model**: the setup, and the reason for each assumption.
3. **What Happens**: run it forward and the main results.
4. **Playground**: change the settings and see what happens.

No maths needed to follow along.
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
