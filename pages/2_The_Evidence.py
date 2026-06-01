"""Page 2 — The Evidence: what's happened since 2024."""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="The Evidence", layout="centered", page_icon="⚖️")

st.title("The Evidence")
st.markdown(
    """
My model makes a claim about mechanism: as a population polarizes, governance
decays, because politicians start optimising for party loyalty instead of the
public good. A model can't prove that's what happened in the real world, but I can
show you the data and let you weigh it.

One caveat up front, in the spirit of "all models are wrong": none of what follows
is a forecast the model produced. It's corroboration. The model gives a reason to
expect these trends, and the data below is what we actually observe.
    """
)

st.subheader("1. Polarization itself is rising")
st.markdown(
    """
Our World in Data tracks a cross-national political polarization score (from the
V-Dem project), defined as the extent to which a society is divided into hostile
political camps. It's the real-world analogue of the bimodal split this model
produces. Higher means more hostile division.
    """
)
components.iframe(
    "https://ourworldindata.org/grapher/political-polarization-score",
    height=600, scrolling=False,
)
st.caption(
    "If the chart doesn't load, open it directly: "
    "[Political polarization score, Our World in Data]"
    "(https://ourworldindata.org/grapher/political-polarization-score)."
)

st.subheader("2. The affective gap is widening")
st.markdown(
    """
This is the affective polarization the model encodes: the hostility that runs
beyond disagreement into dislike of the other side.

By 2025, large majorities felt frustration and anger toward the opposing party:
89% of Democrats and 86% of Republicans said the other party frustrated them, and
81% of Democrats and 70% of Republicans said it made them angry. The gap is also
widening: Pew finds partisan differences in feelings toward the federal government
are wider than at any point since it began asking in 1997, with Democratic anger at
the government reaching 44% in late 2025, above its 34% peak during Trump's first
term.

Sources: [How Americans feel about the two parties (Pew, Oct 2025)]
(https://www.pewresearch.org/politics/2025/10/30/how-americans-feel-about-the-republican-and-democratic-parties/),
and [Feelings about the federal government grow more polarized (Pew, Dec 2025)]
(https://www.pewresearch.org/short-reads/2025/12/04/as-democrats-anger-spikes-americans-feelings-about-the-federal-government-grow-more-polarized/).
    """
)

st.subheader("3. Governance quality is declining")
st.markdown(
    """
This connects to the governance claim in my 2024 argument: a decline in quality as
policymakers prioritize party loyalty over the public good.

Gallup tracked approval of the Republican-controlled Congress from 17% in January
2025 down into the low-to-mid teens after the autumn government shutdown; by April
2026 approval had fallen to 10% and disapproval tied its record high at 86%. More
telling for the mechanism: the party gap in how people rate Congress has never been
wider. In 2025, 61% of Republicans approved of Congress against 6% of Democrats, a
55-point gap, the largest in Gallup's record since 1974. That is less an assessment
of governance on the merits than party loyalty, measured directly.

Sources: [Record party gaps in approval of Congress (Gallup)]
(https://news.gallup.com/poll/693230/record-party-gaps-job-approval-supreme-court-congress.aspx),
and [Disapproval of Congress ties record high at 86% (Gallup)]
(https://news.gallup.com/poll/708722/disapproval-congress-ties-record-high.aspx).
    """
)

st.info(
    "Polarization is rising, hostility is rising, and approval of Congress is now "
    "split by party. None of this proves the model, but it is the world its "
    "mechanism points to."
)

st.divider()
st.page_link("pages/3_The_Model.py", label="Next: The Model", icon="➡️")
