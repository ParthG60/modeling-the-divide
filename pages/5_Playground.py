"""Page 5 — Playground: the interactive simulation. The only page that computes live."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from model import DEM, IND, REP, Params, simulate

PARTY_COLOR = {DEM: "#2563eb", IND: "#7c3aed", REP: "#dc2626"}
PARTY_LABEL = {DEM: "Democrat", IND: "Independent", REP: "Republican"}

st.set_page_config(page_title="Playground", layout="centered", page_icon="⚖️")

# Party shares always sum to 1. Move one slider and the other two rebalance.
PARTY_KEYS = ["share_dem", "share_ind", "share_rep"]
for _k, _v in {"share_dem": 0.331, "share_ind": 0.338, "share_rep": 0.331}.items():
    st.session_state.setdefault(_k, _v)


def _rebalance(changed):
    others = [k for k in PARTY_KEYS if k != changed]
    remaining = max(0.0, 1.0 - st.session_state[changed])
    total = sum(st.session_state[k] for k in others)
    if total <= 1e-9:
        for k in others:
            st.session_state[k] = remaining / 2
    else:
        for k in others:
            st.session_state[k] = st.session_state[k] / total * remaining

st.title("Playground")
st.markdown(
    """
Your turn. Set the dials below, press **Run**, and watch where the population ends
up. Each control changes one rule of the world. The captions tell you what you're
tuning and what it stands for.
    """
)

st.subheader("Set the scene")

c1, c2 = st.columns(2)
with c1:
    exposure = st.slider("Exposure", 0.01, 1.0, 0.10, step=0.01)
    st.caption("How far across the divide people reach to talk. Low means you "
               "mostly hear from people who already agree with you.")
with c2:
    tolerance = st.slider("Tolerance", 0.01, 0.50, 0.10, step=0.01)
    st.caption("How wide a gap a conversation can bridge before it turns hostile "
               "and pushes the two people apart instead of together.")

c3, c4 = st.columns(2)
with c3:
    gini = st.slider("Economic inequality (Gini)", 0.20, 0.70, 0.434, step=0.001,
                     format="%.3f")
    st.caption("Higher inequality shrinks everyone's tolerance "
               "(tolerance = T / Gini). This is the model's economy-to-discourse link.")
with c4:
    responsiveness = st.slider("Responsiveness", 0.01, 1.0, 0.25, step=0.01)
    st.caption("How far a single conversation moves someone's opinion. "
               "Higher means people are more easily swayed each time they talk.")

with st.expander("More settings (population, party mix, elites, run length)"):
    st.markdown("**Party mix**")
    st.caption("Move any one share and the other two rebalance so the total always "
               "stays at 100%. This sets how the population is divided by party.")
    m1, m2, m3 = st.columns(3)
    m1.slider("Democrat", 0.0, 1.0, step=0.01, format="%.2f",
              key="share_dem", on_change=_rebalance, args=("share_dem",))
    m2.slider("Independent", 0.0, 1.0, step=0.01, format="%.2f",
              key="share_ind", on_change=_rebalance, args=("share_ind",))
    m3.slider("Republican", 0.0, 1.0, step=0.01, format="%.2f",
              key="share_rep", on_change=_rebalance, args=("share_rep",))
    dem_p = st.session_state["share_dem"]
    ind_p = st.session_state["share_ind"]
    rep_p = st.session_state["share_rep"]
    st.caption(f"Current mix: {dem_p:.0%} Democrat / {ind_p:.0%} Independent / "
               f"{rep_p:.0%} Republican.")

    st.markdown("**Population size**")
    n_agents = st.slider("Number of people", 100, 1500, 500, step=100)
    st.caption("How many agents in the simulation. Fewer runs faster; the full "
               "dissertation used 5000.")

    st.markdown("**Elites**")
    elite_prop = st.slider("Share who are elites", 0.0, 0.20, 0.05, step=0.01)
    st.caption("Elites cut across all parties (some Democrats, Independents and "
               "Republicans are elites), so this is separate from the party mix. "
               "They have wider reach and a stronger pull, and don't move when they "
               "talk to ordinary people.")
    e1, e2 = st.columns(2)
    impact_mult = e1.slider("Persuasion multiplier", 1.0, 3.0, 1.2, step=0.1)
    prob_mult = e2.slider("Reach multiplier", 1.0, 3.0, 1.2, step=0.1)
    st.caption("Persuasion: how much harder an elite pushes a listener's opinion. "
               "Reach: how much likelier an elite is to be in any conversation.")

    st.markdown("**Run length**")
    r1, r2 = st.columns(2)
    n_steps = r1.slider("Time steps", 50, 1000, 300, step=50)
    seed = r2.number_input("Random seed", value=42, step=1)
    st.caption("Time steps: how long the conversations run. Seed: change it for a "
               "different random run of the same settings.")

run = st.button("Run", type="primary", use_container_width=True)

st.divider()

if not run:
    st.info("Set the dials above and press **Run** to simulate.")
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

    with st.spinner("Running..."):
        result = simulate(params)

    sigma_initial = float(result.polarization[0])
    sigma_final = float(result.polarization[-1])

    m1, m2, m3 = st.columns(3)
    m1.metric("Polarization at start", f"{sigma_initial:.2f}")
    m2.metric("Polarization at end", f"{sigma_final:.2f}", f"{sigma_final - sigma_initial:+.2f}")
    m3.metric("Effective tolerance", f"{result.effective_tolerance:.2f}",
              help="T / Gini. Agents within this opinion distance pull together.")

    if sigma_final >= 0.45:
        st.markdown("**Result: two hard camps.** The middle has emptied out.")
    elif sigma_final <= 0.12:
        st.markdown("**Result: consensus.** The population converged.")
    else:
        st.markdown("**Result: a partial divide.** Some clustering, some middle left.")

    # --- Opinion distribution: start vs end ---
    st.subheader("Where everyone ended up")
    st.caption("Faded bars are the starting opinions; solid bars are where people "
               "landed. Blue Democrat, violet Independent, red Republican.")
    fig_dist = go.Figure()
    for party in [DEM, IND, REP]:
        mask = result.parties == party
        if mask.sum() == 0:
            continue
        fig_dist.add_trace(go.Histogram(
            x=result.opinions_history[0][mask], xbins=dict(start=0, end=1, size=0.025),
            name=f"{PARTY_LABEL[party]} (start)",
            marker_color=PARTY_COLOR[party], opacity=0.25, legendgroup=PARTY_LABEL[party],
        ))
        fig_dist.add_trace(go.Histogram(
            x=result.opinions_history[-1][mask], xbins=dict(start=0, end=1, size=0.025),
            name=f"{PARTY_LABEL[party]} (end)",
            marker_color=PARTY_COLOR[party], opacity=0.9, legendgroup=PARTY_LABEL[party],
        ))
    fig_dist.update_layout(
        barmode="overlay", height=380,
        xaxis_title="Opinion (0 = left, 1 = right)", yaxis_title="People",
        legend=dict(orientation="h", y=-0.25), margin=dict(t=10),
    )
    st.plotly_chart(fig_dist, use_container_width=True)

    # --- Polarization over time ---
    st.subheader("How the divide grew")
    st.caption("The spread of opinions over time. Flat and low means consensus; "
               "rising toward 0.5 means two hard camps.")
    fig_sigma = go.Figure()
    fig_sigma.add_trace(go.Scatter(
        x=np.arange(len(result.polarization)), y=result.polarization,
        mode="lines", line=dict(color="#0f766e", width=3),
    ))
    fig_sigma.update_layout(
        height=300, xaxis_title="Time step", yaxis_title="Polarization (σ)",
        yaxis=dict(range=[0, 0.6]), margin=dict(t=10),
    )
    st.plotly_chart(fig_sigma, use_container_width=True)
