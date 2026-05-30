"""Page 4 — What Happens: run it forward + the two headline findings."""

from pathlib import Path

import streamlit as st

st.set_page_config(page_title="What Happens", layout="centered", page_icon="⚖️")

FIG = Path(__file__).parent.parent / "figures"

st.title("What Happens")
st.markdown(
    """
Now we let the agents interact. Each step, agents bump into each other; if they're
close enough (and tolerant enough) they pull together, and if they're too far apart
they push *away*. Same-party agents always pull together — that's the tribal pull.

Run the base case forward and watch the middle empty out:
    """
)

st.image(str(FIG / "evolution_panel.png"), use_container_width=True,
         caption="A centred population hollows out and hardens into two camps. "
                 "σ (the spread of opinions) is my polarization measure — it climbs "
                 "as the divide widens.")

st.markdown(
    """
That's the core result in one picture: nobody changed the rules, no shock hit the
system — the divide is an **emergent** property of ordinary interactions. The
question I spent most of my time on was *which dials make it worse.* Two findings
stuck with me.
    """
)

st.subheader("Finding 1 — Exposure drives polarization")
st.image(str(FIG / "sensitivity_exposure.png"), use_container_width=True)
st.markdown(
    """
This one is counterintuitive. **More** cross-ideological contact produces **more**
polarization, not less. The reason: when tolerance is limited, hostile encounters
push people apart faster than agreeable ones pull them together. It echoes the
real-world dynamics of echo chambers — and it's why "just expose people to the
other side" can backfire. The countermeasure isn't *more* contact, it's contact
structured to stay inside the tolerance window: genuine **cross-cutting dialogue**,
not a comment-section brawl.
    """
)

st.subheader("Finding 2 — Inequality polarizes, through tolerance")
st.image(str(FIG / "sensitivity_gini.png"), use_container_width=True)
st.markdown(
    """
This is the part of the dissertation I'm proudest of. Tolerance isn't a fixed
personality trait in my model — it **shrinks as economic inequality rises**, on the
premise that *higher inequality is accompanied by poorer feelings toward politics.*
A single macro number (the Gini coefficient) silently re-scales the threshold every
interaction is judged against.

The consequence is direct: **lower inequality → higher tolerance → less
polarization** — and at low enough inequality, the population barely splits at all.
As I put it in the dissertation, this points to the *"necessity of addressing
economic disparities as part of any comprehensive strategy to mitigate societal
polarization."* The lever isn't only in the discourse; it's partly in the economy.
    """
)

st.subheader("And the quiet hero: independents")
st.markdown(
    """
One thing that genuinely surprised me: cranking up *responsiveness* or *elite
influence* didn't reliably increase polarization. Digging in, the reason was the
moderate bloc — **independents act as a damper**, tempering the elite-driven push
toward the extremes. They're easy to dismiss as noise; in the model they're a
structural brake on the divide.
    """
)

st.success(
    "That's the guided tour. Everything above came from fixed settings — but the "
    "model has a dozen dials. **Head to the Playground** to set your own scenario "
    "and see if you can make the divide collapse, explode, or hold steady. →"
)
