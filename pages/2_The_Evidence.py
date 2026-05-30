"""Page 2 — The Evidence: what's happened since 2024."""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="The Evidence", layout="centered", page_icon="⚖️")

st.title("The Evidence")
st.markdown(
    """
My model makes a claim about *mechanism*: as a population polarizes, governance
decays, because politicians start optimising for party loyalty instead of the
public good. A model can't prove that's what happened in the real world — but I
can show you the data and let you decide whether the mechanism is doing real work.

A caveat up front, in the spirit of "all models are wrong": none of what follows
is a forecast the model produced. It's corroboration. The model gives a *reason*
to expect these trends; the data below is what we actually observe.
    """
)

st.subheader("1. Polarization itself is rising")
st.markdown(
    """
Our World in Data tracks a cross-national **political polarization score** (from
the V-Dem project) — literally *"the extent to which society is divided into
hostile political camps."* It's the real-world analogue of the bimodal split this
model produces. Higher = more hostile division.
    """
)
components.iframe(
    "https://ourworldindata.org/grapher/political-polarization-score",
    height=600, scrolling=False,
)
st.caption(
    "If the chart doesn't load, open it directly: "
    "[Political polarization score — Our World in Data]"
    "(https://ourworldindata.org/grapher/political-polarization-score)."
)

st.subheader("2. The affective gap is widening")
st.markdown(
    """
This is the *affective* polarization the model encodes — not just disagreement, but
hostility toward the other side.

- Pew finds the share of partisans who view the opposing party as **more immoral**
  than other Americans rose to **72% of Republicans and 63% of Democrats (2022)**,
  up from just **47% and 35% in 2016**.
- In **December 2025**, Pew reported Americans' feelings about the federal
  government have grown **more polarized**, with partisan anger spiking.

Sources: [How Americans feel about the two parties (Pew, Oct 2025)]
(https://www.pewresearch.org/politics/2025/10/30/how-americans-feel-about-the-republican-and-democratic-parties/)
· [Feelings about the federal government grow more polarized (Pew, Dec 2025)]
(https://www.pewresearch.org/short-reads/2025/12/04/as-democrats-anger-spikes-americans-feelings-about-the-federal-government-grow-more-polarized/)
    """
)

st.subheader("3. Governance quality is paying the price")
st.markdown(
    """
This is the part of my 2024 thesis I find most striking in hindsight — *"a decline
in the quality of governance, as policymakers prioritize party loyalty over the
public good."*

- Gallup put **Congressional approval at ~17% in December 2025**, with disapproval
  later **tying its record high at 86%**.
- More telling for the *mechanism*: Gallup reports the party gap in how people rate
  Congress has **"never been more divergent by party."** Republicans approved of
  Congress at ~61% when their party held power — versus single digits for the other
  side. That's not citizens judging governance on the merits; that's **party loyalty
  over the public good**, measured directly. It's the pandering dynamic in one chart.

Sources: [Record party gaps in approval of Congress (Gallup)]
(https://news.gallup.com/poll/693230/record-party-gaps-job-approval-supreme-court-congress.aspx)
· [Disapproval of Congress ties record high at 86% (Gallup)]
(https://news.gallup.com/poll/708722/disapproval-congress-ties-record-high.aspx)
    """
)

st.info(
    "So: polarization up, hostility up, governance trust collapsing along party "
    "lines. None of it proves the model — but it's exactly the world the model's "
    "mechanism predicts. **Next: how the model actually works.** →"
)
