"""Page 4 — What Happens: run it forward, the two drivers, and the honest
independents story."""

from pathlib import Path

import streamlit as st

st.set_page_config(page_title="What Happens", layout="centered", page_icon="⚖️")

FIG = Path(__file__).parent.parent / "figures"

st.title("What Happens")
st.markdown(
    """
Now we let the agents talk. Each step they bump into each other. If they're close
enough (and tolerant enough) they drift together; if they're too far apart they
push away. Same-party agents always drift together. Run the base case forward and
watch the middle empty out.
    """
)

st.image(str(FIG / "evolution_panel.png"), use_container_width=True,
         caption="A centred population hollows out and hardens into two camps. "
                 "σ, the spread of opinions, is the polarization measure: it climbs "
                 "as the divide widens.")

st.markdown(
    """
That's the core result in one picture. Nobody changed the rules and no shock hit
the system. The divide simply emerges from ordinary interactions. The question I
spent most of my time on was which dials make it worse. Two answers stuck with me.
    """
)

st.subheader("Driver 1: exposure")
st.image(str(FIG / "sensitivity_exposure.png"), use_container_width=True)
st.markdown(
    """
This one is counterintuitive. *More* contact across the divide produces *more*
polarization, not less. When tolerance is limited, hostile encounters push people
apart faster than friendly ones pull them together. It's the echo-chamber result
seen from the other side, and it's why "just expose people to the other view" can
backfire. The fix isn't more contact, it's contact kept inside the tolerance
window: real cross-cutting dialogue rather than a comment-section brawl.
    """
)

st.subheader("Driver 2: inequality")
st.image(str(FIG / "sensitivity_gini.png"), use_container_width=True)
st.markdown(
    """
This is the part of the dissertation I'm proudest of. Tolerance isn't a fixed trait
here. It shrinks as economic inequality rises, on the premise that feeling the gap
sours people on politics generally. So a single macro number, the Gini coefficient,
re-scales the threshold every interaction is judged against. Lower inequality buys
higher tolerance and a calmer population; at low enough inequality the divide barely
forms at all. The lever isn't only in the discourse. Part of it sits in the economy.
    """
)

st.subheader("The independents surprised me, twice")
st.markdown(
    """
In the original dissertation, independents looked like the heroes. Cranking up
elite influence or responsiveness didn't reliably raise polarization, and I put
that down to the centrist bloc absorbing the shock: independents as a damper on
elite-driven extremes.

When I rebuilt the model for this app, I went looking for that result again, and
I want to be straight with you: **in this lighter version it isn't there.** I tested
it across exposure, tolerance, elite influence, and even interaction density (from
one conversation per step all the way up to everyone-meets-everyone). Adding
independents doesn't calm the population. If anything it nudges polarization
slightly *up*. The tempering effect lived in the full model (5000 agents, every
pair interacting, thousands of steps) and didn't survive the simplifications that
make this version fast. That's a real lesson about models, and the two quotes on
the first page were earning their keep: all models are wrong, and a result that
holds in one specification can quietly flip in another.

But the more interesting thing is what the model shows *instead*, and this part is
rock-solid across every setting I tried:
    """
)

st.image(str(FIG / "independents_capture.png"), use_container_width=True,
         caption="Independents start as the centre and end at the extremes.")

st.markdown(
    """
Independents don't hold the middle. They get captured by it. At the start, just over
half of them sit in the centre. By the end, almost none do: about 3% remain, and the
rest have been pulled into one camp or the other, split close to evenly between left
and right. The people with no allegiance turn out to be the most up for grabs, and a
polarizing system doesn't get calmed by them. It swallows them.

I find that bleaker and more honest than the tidy "moderates save us" story. Nobody
stays neutral. The middle isn't a stable place to stand; it's the ground both sides
fight over until it's gone.
    """
)

st.success(
    "That's the guided tour. Everything above came from fixed settings, but the "
    "model has a dozen dials. Head to the **Playground** to set your own scenario "
    "and see if you can make the divide collapse, explode, or hold steady."
)

st.divider()
st.page_link("pages/5_Playground.py", label="Next: open the Playground", icon="➡️")
