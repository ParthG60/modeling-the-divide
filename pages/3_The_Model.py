"""Page 3 — The Model: setup, intuition, and the maths (appendix)."""

from pathlib import Path

import streamlit as st

st.set_page_config(page_title="The Model", layout="centered", page_icon="⚖️")

FIG = Path(__file__).parent.parent / "figures"

st.title("The Model")
st.markdown(
    """
The model follows a principle the modelling literature calls *input realism*:
every assumption should trace back to real data or established theory rather than a
guess. Before anything moves, here is where the population starts and why it looks
the way it does.

Each agent sits somewhere on a left-to-right opinion line from 0 to 1, and carries
two labels. The first is a **party**: Democrat, Independent, or Republican. The
second is whether they are an **elite** (a pundit, politician, or high-reach
account) or one of the **masses**. That is the whole cast.
    """
)

st.image(str(FIG / "initial_distribution.png"), use_container_width=True,
         caption="The starting population at t = 0. Blue Democrats lean left, "
                 "red Republicans lean right, violet Independents sit in the middle.")

st.subheader("Why it starts already leaning")
st.markdown(
    """
Notice the population doesn't begin neutral. Democrats cluster around 0.35 and
Republicans around 0.65, with a populated but thinning middle. That isn't me
tipping the scales. It's what the survey data shows: opinion in the US is already
bimodal, on both ideological and emotional measures (Enders, 2021). I anchor the
party split and the roughly one-third / one-third / one-third proportions to ANES
data, and hold them fixed in every run.
    """
)

st.subheader("Why elites sit further out")
st.markdown(
    """
The same evidence shows that elites are more polarized than the people they
represent. So elite agents get a wider spread, with more of them near the edges. I
left their average where the masses' is and only widened the variance, so the split
emerges from the dynamics rather than being assumed at the start.
    """
)

st.subheader("Why independents start in the middle")
st.markdown(
    """
Independents are the bloc with no strong allegiance, common across democracies and
well documented in the US, so I centre them at 0.5. One caveat: I gave independent
elites and independent masses the same spread, because I found no evidence to
justify treating them differently. How this centrist bloc behaves once the
simulation runs is covered on the next page.
    """
)

st.subheader("How a conversation works")
st.markdown(
    """
Each step, agents bump into one another. Two things govern what happens:

1. **Who talks to whom.** The closer two opinions are, the likelier they interact.
   How steeply that probability falls with distance is the **Exposure** dial: turn
   it up and people reach further across the divide to talk.
2. **What a conversation does.** If two people are within a **tolerance** window,
   the exchange pulls them together. If they're outside it, the exchange pushes
   them apart. Same-party agents always pull together, tribally, no matter the gap.

The less obvious part is that tolerance is not a fixed trait. It shrinks as economic
inequality rises, so the Gini coefficient re-scales the threshold that every
interaction is judged against. More inequality means thinner tolerance and more
repulsion. That is the link between the economy and the discourse.

Independents are treated as less polarizing throughout: they move normally when
drawn toward someone but only weakly when pushed away, which keeps them from being
dragged to the extremes.
    """
)

with st.expander("Appendix: the full rules and the maths"):
    st.markdown(r"""
The model extends Axelrod-style opinion dynamics with three additions: an
elite/mass split with different behaviour, a tolerance threshold scaled by economic
inequality, and an explicit role for independents.

**Initial distribution (Eq. 2.1).** Each agent's starting opinion is drawn from a
group-specific normal:

$$
x_i(0) \sim \begin{cases}
\mathcal{N}(0.5,\, 0.2^2)   & \text{Independent} \\
\mathcal{N}(0.35,\, 0.15^2) & \text{Mass Democrat} \\
\mathcal{N}(0.65,\, 0.15^2) & \text{Mass Republican} \\
\mathcal{N}(0.35,\, 0.2^2)  & \text{Elite Democrat} \\
\mathcal{N}(0.65,\, 0.2^2)  & \text{Elite Republican}
\end{cases}
$$

**Interaction probability (Eq. 2.2).** For a pair $(i,j)$ at opinion distance
$d = |x_i - x_j|$, with $E$ the Exposure parameter and a multiplier $m_{\text{prob}}$
applied when either agent is an elite:

$$
p_{ij} = \left(\tfrac{1}{2}\right)^{d/E} \cdot m_{\text{prob}}^{\mathbb{1}[\text{elite}]}
$$

**Opinion update (Eq. 2.3).** If the interaction fires:

$$
x_i(t+1) = x_i(t) + s \cdot R \cdot (x_j(t) - x_i(t)) \cdot k
$$

where $s \in \{+1,-1\}$ is attract or repel, $R$ is **Responsiveness**, and
$k \in \{m_\text{imp}, 1, 1/m_\text{imp}\}$ is the strong / regular / weak modifier.

**Tolerance (Eq. 2.4).** The effective tolerance is inversely scaled by inequality:

$$
\text{Tolerance} = \frac{T}{\text{Gini}}, \qquad \text{Gini}_{\text{base}} = 0.434
$$

**Which influence type fires (Table 2.2):**

| Type | Condition |
|---|---|
| Strong positive | Same-party partisans, Elite + Mass |
| Regular positive | Same-party same-status; both Independents within tolerance; different-party Elite + Mass within tolerance; Partisan-Elite + Independent-Mass within tolerance |
| Weak positive | Same-status, different-party partisans, within tolerance |
| Strong negative | Different-party partisans, Elite + Mass, outside tolerance |
| Regular negative | Different-party same-status, outside tolerance |
| Weak negative | Any interaction involving an independent, outside tolerance |

Three rules sit on top: same-party partisans *always* attract (tribalism, ignoring
tolerance); elites *don't move* when they talk to the masses (only the listener
shifts); and interactions involving independents repel only weakly, so independents
resist being pushed to the extremes. That last rule is what makes independents a
moderating force.

**Implementation note.** The dissertation ran $N = 5000$ agents over up to 2000
steps, with every pair interacting each step (about 12.5 million pairings per step).
That is too heavy for a web app, so this version uses a smaller $N$ and has each
agent talk to one random partner per step instead of all pairs. The per-interaction
rules are identical and the dynamics are equivalent in expectation, though you may
need more steps to reach the same place.

> *Goyal, P. (2024). Modeling the Divide: Mathematical Approaches to Understanding
> and Mitigating Political Polarization. BSc (Hons) Mathematics & Statistics,
> University of St Andrews.*
""")

st.divider()
st.page_link("pages/4_What_Happens.py", label="Next: What Happens", icon="➡️")
