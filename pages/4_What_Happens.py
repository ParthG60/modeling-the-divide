"""Page 4 — What Happens: run it forward, the two drivers, and the independents result."""

from pathlib import Path

import streamlit as st

st.set_page_config(page_title="What Happens", layout="centered", page_icon="⚖️")

FIG = Path(__file__).parent.parent / "figures"

st.title("What Happens")
st.markdown(
    """
Now we let the agents talk. Each step they meet other agents. If they are close
enough, and tolerant enough, they move toward each other; if they are too far
apart, they move away. Same-party agents always move together. Run the base case
forward and the middle thins out.
    """
)

st.image(str(FIG / "evolution_panel.png"), use_container_width=True,
         caption="A centred population separates into two camps. σ, the spread of "
                 "opinions, rises from about 0.22 to 0.43 here as the divide widens.")

st.markdown(
    """
I measure polarization with σ, the standard deviation of opinions. It is near zero
when everyone agrees and reaches its maximum of 0.5 when the population splits
evenly into two camps at opposite ends of the scale, so it measures what we care
about: how far opinions have spread toward the extremes. It is the
measure the dissertation used. It has one blind spot: it can't tell a smooth
spread from a clean two-camp split, and it reads low when a divide is lopsided and
one side holds most of the people. So in the Playground I pair it with the share
of people at the extremes, and with the opinion distribution itself, which shows
the shape directly.

No rule changed and no external shock hit the system. The divide emerges from
ordinary interactions. The next question is which settings make it worse. Two
matter most.
    """
)

st.subheader("Driver 1: exposure")
st.image(str(FIG / "sensitivity_exposure.png"), use_container_width=True,
         caption="Final polarization (σ) rises with exposure: more contact across "
                 "the divide brings more hostile encounters, not fewer.")
st.markdown(
    """
More contact across the divide produces more polarization, not less. When
tolerance is limited, hostile encounters push people apart faster than friendly
ones bring them together. This is the echo-chamber result, and it is why simply
exposing people to the other side can backfire. What helps is
contact that stays inside the tolerance window, where the exchange pulls people
together rather than apart.
    """
)

st.subheader("Driver 2: inequality")
st.image(str(FIG / "sensitivity_gini.png"), use_container_width=True,
         caption="Final polarization (σ) rises with inequality: a higher Gini "
                 "shrinks tolerance, so the divide widens. At low inequality it "
                 "barely forms.")
st.markdown(
    """
Tolerance is not fixed in the model. It shrinks as economic inequality rises, on
the assumption that a wider gap sours people on politics in general. So the Gini
coefficient re-scales the threshold every interaction is judged against. Lower
inequality means higher tolerance and a calmer population; at low enough inequality
the divide barely forms. That makes inequality an economic lever on a political
problem.
    """
)

st.subheader("Independents slow the divide")
st.markdown(
    """
The dissertation's other main finding was that independents act as a brake on
polarization, and the model reproduces it. Independents have no party to be loyal
to, and the rules treat them asymmetrically: when an independent is drawn toward
someone they move at full strength, but when they are pushed away they move only
weakly. That asymmetry means independents resist being dragged to the extremes,
and a large enough bloc of them keeps pulling the rest of the population back
toward the centre.
    """
)

st.image(str(FIG / "independents_dampen.png"), use_container_width=True,
         caption="Final polarization falls as independents make up more of the "
                 "population, from about σ = 0.38 with none to about 0.29 at 70%. "
                 "The band shows variation across runs.")

st.markdown(
    """
The effect is modest at first. Below about a third of the population, independents
make little difference. Above that, the final divide shrinks steadily as their
share grows. The United States sits near that one-third mark, roughly where the
effect begins to matter, which is part of why a wider, less partisan middle is one
of the few things in the model that slows the divide.
    """
)

st.success(
    "That is the guided tour. Everything above used fixed settings, but the model "
    "has a dozen dials. Open the Playground to set your own scenario and see what "
    "the population does."
)

st.divider()
st.page_link("pages/5_Playground.py", label="Next: open the Playground", icon="➡️")
