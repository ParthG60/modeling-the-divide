"""Page 3 — The Model: the starting setup and why each assumption is made."""

from pathlib import Path

import streamlit as st

st.set_page_config(page_title="The Model", layout="centered", page_icon="⚖️")

FIG = Path(__file__).parent.parent / "figures"

st.title("The Model")
st.markdown(
    """
My guiding principle was something the modelling literature calls **"input
realism"**: every assumption should be traceable to real data or established
theory, not pulled from thin air. So before anything moves, let me walk you through
where the population *starts* — and why I set it up this way.

Each agent sits on a **left–right opinion line from 0 to 1**, and carries two
labels: a **party** (Democrat, Independent, Republican) and an **elite / mass**
status. Here's the starting distribution:
    """
)

st.image(str(FIG / "initial_distribution.png"), use_container_width=True,
         caption="The initial population (t = 0): already leaning, but with a "
                 "populated middle. Blue = Democrat, grey = Independent, red = Republican.")

st.subheader("Why it starts bimodal")
st.markdown(
    """
The population doesn't start neutral — it starts *already leaning*, with Democrats
clustered left (around 0.35) and Republicans right (around 0.65). That's not me
putting my thumb on the scale; it's what the data shows. Enders (2021) documents
that opinion in the US is already **bimodal** on both ideological and affective
measures. I anchor the party split and proportions (≈33% / 34% / 33%) to ANES
survey data and hold them fixed across every run.
    """
)

st.subheader("Why elites get fatter tails")
st.markdown(
    """
The same evidence shows something I found important: **elites are *more* polarized
than the masses they represent.** So elite agents (pundits, politicians, very-online
accounts — a small minority) get a wider opinion variance: fatter tails, more of
them out at the edges. I deliberately *didn't* shift their average further out — I
only widened the spread — to avoid baking in the very bimodality I wanted the model
to *produce*, not assume.
    """
)

st.subheader("Why independents sit in the middle")
st.markdown(
    """
Independents are a non-partisan bloc — common across democracies and well
documented in the US — so I centre them at 0.5 with no built-in lean. I'll be
honest about a modeller's choice here: I gave independent elites and independent
masses the *same* variance, simply because I couldn't find evidence to justify
treating them differently. As you'll see on the next page, this unassuming bloc in
the middle turns out to matter more than I expected.
    """
)

st.markdown(
    """
---
That's the whole setup: a leaning-but-not-yet-split population, with a more extreme
elite minority and a moderate centre. Now the interesting question — **what happens
when you let them talk to each other?** →
    """
)
