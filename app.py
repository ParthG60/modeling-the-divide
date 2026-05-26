"""
Streamlit interface for the polarization ABM.
Run locally:   streamlit run app.py
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from model import DEM, IND, REP, Params, simulate

PARTY_COLOR = {DEM: "#1f77b4", IND: "#888888", REP: "#d62728"}
PARTY_LABEL = {DEM: "Democrat", IND: "Independent", REP: "Republican"}

st.set_page_config(page_title="Modeling the Divide", layout="wide", page_icon="⚖️")

# ==============================================================================
# Header (shared across tabs)
# ==============================================================================
st.title("Modeling the Divide")
st.caption(
    "An interactive playground for the agent-based polarization model from my "
    "2024 St Andrews dissertation."
)

tab_idea, tab_play, tab_method = st.tabs(["The Idea", "Playground", "Methodology"])

# ==============================================================================
# TAB 1 — THE IDEA (landing page, intuition only)
# ==============================================================================
with tab_idea:
    st.markdown(
        """
### The question

Why does a population split into hardened tribes? Not because individuals
suddenly become extreme, but because of the *rules* by which they bump into
each other and update their views.

This model is the simplest version of that idea I could make work: a few
hundred agents on a left–right spectrum, with rules for who talks to whom and
how they shift after each conversation. Run it forward and the population
sometimes converges, sometimes splits cleanly into two camps, sometimes
something in between — depending on the dials.

### The three dials that matter most

- **Exposure** — How willing are you to talk to someone with a different
  opinion? Crank it up and the population mixes harder. Counterintuitively,
  more mixing often means *more* polarization, not less: hostile contact
  pushes people apart faster than agreeable contact pulls them together.

- **Tolerance** — How far apart can two opinions be before a conversation
  turns hostile instead of constructive? Inside the tolerance window, you
  shift toward each other. Outside, you shift away.

- **Inequality** — Tolerance isn't a fixed personal trait in the model. It
  shrinks as economic inequality (Gini) rises. This is the dissertation's
  key move: a single macro number — how unequal the society is — silently
  re-scales the threshold every individual interaction is measured against.

There are a few other dials (responsiveness, elite influence, party mix)
but those three carry most of the dynamics.

### Three kinds of agent

Agents come in three flavours that interact differently:

- **Partisans** (Democrats and Republicans) start with a clear lean and a
  tribal pull toward their own side. Same-party agents *always* attract,
  regardless of how far apart they are.
- **Independents** start in the middle with no tribe. They tend to
  *moderate* extremes — and one of the original findings was just how much.
- **Elites** are a small slice of the population (think pundits,
  politicians, very-online accounts) with broader reach and stronger pull.
  When an elite talks to a regular person, the elite doesn't budge — only
  the listener does.

### What you can do

Go to **Playground** and move the sliders. Try:

1. **Default** — see baseline polarization emerge.
2. **Crank up exposure** — watch polarization accelerate.
3. **Drop Gini to 0.25** — watch polarization collapse, sometimes into
   consensus. This is the headline finding: *lower inequality → higher
   effective tolerance → less polarization.*
4. **Set responsiveness very high** — and watch nothing dramatic happen,
   because independents temper it.

The maths and exact rules are in **Methodology**. You don't need them to
play with the model.
        """
    )

# ==============================================================================
# TAB 2 — PLAYGROUND (sidebar + sim)
# ==============================================================================
with tab_play:
    st.sidebar.title("Parameters")
    st.sidebar.caption("Tweak the knobs, rerun, watch the divide form (or not).")

    with st.sidebar.expander("Population", expanded=True):
        n_agents = st.slider("Number of agents (N)", 100, 1500, 500, step=100,
                            help="Dissertation used N=5000; we use fewer to keep it interactive.")
        elite_prop = st.slider("Elite proportion", 0.0, 0.20, 0.05, step=0.01,
                              help="Fraction of agents with elite status.")
        col1, col2, col3 = st.columns(3)
        dem_p = col1.number_input("% Dem", 0.0, 1.0, 0.331, step=0.01, format="%.3f")
        ind_p = col2.number_input("% Ind", 0.0, 1.0, 0.338, step=0.01, format="%.3f")
        rep_p = col3.number_input("% Rep", 0.0, 1.0, 0.331, step=0.01, format="%.3f")

    with st.sidebar.expander("Core parameters", expanded=True):
        exposure = st.slider("Exposure (E)", 0.01, 1.0, 0.10, step=0.01,
                            help="Higher E → agents interact across larger opinion gaps.")
        tolerance = st.slider("Tolerance (T)", 0.01, 0.50, 0.10, step=0.01,
                             help="Within effective tolerance → attract. Outside → repel.")
        responsiveness = st.slider("Responsiveness (R)", 0.01, 1.0, 0.25, step=0.01,
                                  help="How much an opinion shifts per interaction.")
        gini = st.slider("Gini coefficient", 0.20, 0.70, 0.434, step=0.001, format="%.3f",
                        help="Effective tolerance = T / Gini. Higher inequality → less tolerance.")

    with st.sidebar.expander("Elite influence"):
        impact_mult = st.slider("Impact multiplier", 1.0, 3.0, 1.2, step=0.1)
        prob_mult = st.slider("Probability multiplier", 1.0, 3.0, 1.2, step=0.1)

    with st.sidebar.expander("Simulation"):
        n_steps = st.slider("Time steps", 50, 1000, 300, step=50)
        seed = st.number_input("Random seed", value=42, step=1)

    run = st.sidebar.button("Run simulation", type="primary", use_container_width=True)

    if not run:
        st.info("Set parameters in the sidebar and hit **Run simulation**.")
    else:
        params = Params(
            n_agents=n_agents,
            dem_proportion=dem_p, ind_proportion=ind_p, rep_proportion=rep_p,
            elite_proportion=elite_prop,
            exposure=exposure, tolerance=tolerance,
            responsiveness=responsiveness, gini=gini,
            impact_multiplier=impact_mult, prob_multiplier=prob_mult,
            n_steps=int(n_steps), seed=int(seed),
        )

        with st.spinner("Running simulation..."):
            result = simulate(params)

        sigma_initial = float(result.polarization[0])
        sigma_final = float(result.polarization[-1])
        eff_tol = result.effective_tolerance

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Initial σ", f"{sigma_initial:.3f}")
        c2.metric("Final σ", f"{sigma_final:.3f}", f"{sigma_final - sigma_initial:+.3f}")
        c3.metric("Effective tolerance", f"{eff_tol:.3f}",
                  help="T / Gini — agents within this opinion distance attract.")
        c4.metric("Elite agents", int(result.is_elite.sum()))

        # --- Opinion distribution: initial vs final ---
        st.subheader("Opinion distribution: initial vs final")
        fig_dist = go.Figure()
        for party in [DEM, IND, REP]:
            mask = result.parties == party
            if mask.sum() == 0:
                continue
            fig_dist.add_trace(go.Histogram(
                x=result.opinions_history[0][mask], xbins=dict(start=0, end=1, size=0.025),
                name=f"{PARTY_LABEL[party]} (initial)",
                marker_color=PARTY_COLOR[party], opacity=0.25,
                legendgroup=PARTY_LABEL[party],
            ))
            fig_dist.add_trace(go.Histogram(
                x=result.opinions_history[-1][mask], xbins=dict(start=0, end=1, size=0.025),
                name=f"{PARTY_LABEL[party]} (final)",
                marker_color=PARTY_COLOR[party], opacity=0.85,
                legendgroup=PARTY_LABEL[party],
            ))
        fig_dist.update_layout(
            barmode="overlay", height=420,
            xaxis_title="Opinion (0 = left, 1 = right)", yaxis_title="Agents",
            legend=dict(orientation="h", y=-0.2),
        )
        st.plotly_chart(fig_dist, use_container_width=True)

        # --- Polarization over time ---
        st.subheader("Polarization over time (σ of opinions)")
        fig_sigma = go.Figure()
        fig_sigma.add_trace(go.Scatter(
            x=np.arange(len(result.polarization)), y=result.polarization,
            mode="lines", line=dict(color="#222", width=2), name="σ(opinions)",
        ))
        fig_sigma.update_layout(
            height=320, xaxis_title="Time step", yaxis_title="Std dev of opinions",
            yaxis=dict(range=[0, 0.6]),
        )
        st.plotly_chart(fig_sigma, use_container_width=True)

        # --- Trajectories ---
        st.subheader("Opinion trajectories (sample of agents)")
        sample_size = min(40, params.n_agents)
        sample_idx = np.random.default_rng(0).choice(params.n_agents, sample_size, replace=False)
        max_points = 120
        step_size = max(1, result.opinions_history.shape[0] // max_points)
        t_axis = np.arange(0, result.opinions_history.shape[0], step_size)
        traj = result.opinions_history[t_axis][:, sample_idx]

        fig_traj = go.Figure()
        for k, idx in enumerate(sample_idx):
            color = PARTY_COLOR[int(result.parties[idx])]
            fig_traj.add_trace(go.Scatter(
                x=t_axis, y=traj[:, k], mode="lines",
                line=dict(color=color, width=1.6 if result.is_elite[idx] else 0.8),
                opacity=0.95 if result.is_elite[idx] else 0.4,
                showlegend=False, hoverinfo="skip",
            ))
        fig_traj.update_layout(
            height=360, xaxis_title="Time step", yaxis_title="Opinion",
            yaxis=dict(range=[0, 1]),
        )
        st.plotly_chart(fig_traj, use_container_width=True)
        st.caption("Each line is one agent. Bold lines = elites. "
                   "Color = party (blue Dem, grey Ind, red Rep).")

# ==============================================================================
# TAB 3 — METHODOLOGY (the rigorous detail)
# ==============================================================================
with tab_method:
    st.markdown(r"""
## Source

This is the agent-based model from my undergraduate dissertation:

> **Goyal, P. (2024).** *Modeling the Divide: Mathematical Approaches to
> Understanding and Mitigating Political Polarization.* BSc (Hons)
> Mathematics & Statistics, University of St Andrews.

The dissertation builds on Axelrod-style opinion-dynamics ABMs and adds three
things: elite/mass stratification with differential rules, a tolerance
threshold scaled by economic inequality, and an explicit independent-moderator
role.

## Agents

Each agent has an opinion $x_i \in [0, 1]$ and two attributes:

- **Party**: Democrat / Independent / Republican (ANES-informed proportions
  ~33.1% / 33.8% / 33.1%).
- **Elite status**: binary. Elites get a probability boost (denser networks)
  and an impact boost (stronger pull) — but they *don't move* themselves
  when interacting with mass agents.

## Equation 2.1 — Initial distribution

$$
x_i(0) \sim \begin{cases}
\mathcal{N}(0.5,\, 0.2^2)   & \text{Independent} \\
\mathcal{N}(0.35,\, 0.15^2) & \text{Mass Democrat} \\
\mathcal{N}(0.65,\, 0.15^2) & \text{Mass Republican} \\
\mathcal{N}(0.35,\, 0.2^2)  & \text{Elite Democrat} \\
\mathcal{N}(0.65,\, 0.2^2)  & \text{Elite Republican}
\end{cases}
$$

Elite distributions have fatter tails — empirically (Enders 2021) elites are
more polarized than the masses they represent.

## Equation 2.2 — Interaction probability

For a pair $(i, j)$ with opinion distance $d = |x_i - x_j|$:

$$
p_{ij} = \left(\tfrac{1}{2}\right)^{d / E} \cdot m_{\text{prob}}^{\mathbb{1}[\text{elite}]}
$$

$E$ is **Exposure**; $m_{\text{prob}}$ is the elite probability multiplier.

## Equation 2.3 — Opinion update

If the interaction fires, agent $i$'s opinion updates as:

$$
x_i(t+1) = x_i(t) + s \cdot R \cdot (x_j(t) - x_i(t)) \cdot k
$$

- $s \in \{+1, -1\}$: attract or repel (set by the influence type below)
- $R$: **Responsiveness** (magnitude per interaction)
- $k \in \{m_\text{imp},\, 1,\, 1/m_\text{imp}\}$: strength modifier — **strong**,
  **regular**, or **weak**

## Equation 2.4 — Tolerance scaling

$$
\text{Tolerance} = \frac{T}{\text{Gini}}
$$

The dissertation's key novelty: the effective tolerance threshold is *inversely*
scaled by economic inequality. Higher inequality → lower tolerance → wider
repulsion zone. Default Gini = 0.434 (latest US estimate at the time).

## Table 2.2 — When does each influence type fire?

| Influence type | Condition |
|---|---|
| **Strong positive** | Same-party partisans, Elite + Mass |
| **Regular positive** | Same-party same-status; both Independents (same status) within tolerance; different-party Elite + Mass within tolerance; Partisan-Elite + Independent-Mass within tolerance |
| **Weak positive** | Same-status, different-party partisans, within tolerance |
| **Strong negative** | Different-party partisans, Elite + Mass, outside tolerance |
| **Regular negative** | Different-party same-status outside tolerance; Partisan-Elite + Independent-Mass outside tolerance |
| **Weak negative** | Both Independents, outside tolerance |

Two rules to keep in mind:

- **Same-party partisans always attract**, regardless of tolerance (tribalism).
- **Elites stay fixed** when interacting with masses; only the mass agent updates.

---

## Implementation notes

The dissertation ran $N = 5000$ agents over 500–2000 timesteps, with each
timestep iterating over all $\binom{N}{2} \approx 12.5\text{M}$ pairs. That's
fine for offline experiments but doesn't fit a sub-second interactive app.
Two pragmatic adjustments:

1. **Smaller $N$** (100–1500, default 500) — big enough to see distributions,
   small enough to run in a couple of seconds.
2. **Random-partner update** instead of all-pairs: each step every agent picks
   one random partner and (probabilistically) interacts. Same per-interaction
   rules, fewer pair-evaluations per step. Equivalent dynamics in expectation;
   you may want more timesteps to reach the same equilibrium.

Everything else — initial distributions, the 6 influence rules, the elite
asymmetry, the Gini-scaled tolerance, the same-party tribalism rule — is
verbatim from the dissertation.

## Original findings (from the dissertation)

1. **Exposure → polarization** (monotonic). More cross-ideological contact
   drives clustering into extremes.
2. **Inequality → polarization, through tolerance.** Lower Gini → higher
   tolerance → convergence; higher Gini → less tolerance → repulsion.
3. **Responsiveness and Elite Impact don't behave monotonically.**
   Independents systematically temper what naive intuition would predict.
4. **Initial conditions matter a lot.** Reduce starting partisanship and
   polarization slows dramatically; skew the start slightly and it accelerates.
""")
