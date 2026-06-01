"""Page 5 — Playground: the interactive simulation. The only page that computes live."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from model import DEM, IND, REP, Params, simulate

PARTY_COLOR = {DEM: "#2563eb", IND: "#7c3aed", REP: "#dc2626"}
PARTY_LABEL = {DEM: "Democrat", IND: "Independent", REP: "Republican"}

st.set_page_config(page_title="Playground", layout="centered", page_icon="⚖️")

# The population mix (parties + elites) always sums to 1. Move one share and the
# rest rebalance proportionally so the total stays at 100%.
GROUP_KEYS = ["share_dem", "share_ind", "share_rep", "share_elite"]
for _k, _v in {"share_dem": 0.31, "share_ind": 0.33, "share_rep": 0.31,
               "share_elite": 0.05}.items():
    st.session_state.setdefault(_k, _v)


def _rebalance(changed):
    others = [k for k in GROUP_KEYS if k != changed]
    remaining = max(0.0, 1.0 - st.session_state[changed])
    total = sum(st.session_state[k] for k in others)
    if total <= 1e-9:
        for k in others:
            st.session_state[k] = remaining / len(others)
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

with st.expander("More settings (population mix, elites, run length)"):
    st.markdown("**Population mix**")
    st.caption("These four shares are the make-up of the population and always sum "
               "to 100%. Move any one and the rest rebalance. Elites are spread "
               "across the parties, so raising the elite share lowers the others.")
    g1, g2 = st.columns(2)
    g1.slider("Democrats", 0.0, 1.0, step=0.01, format="%.2f",
              key="share_dem", on_change=_rebalance, args=("share_dem",))
    g2.slider("Independents", 0.0, 1.0, step=0.01, format="%.2f",
              key="share_ind", on_change=_rebalance, args=("share_ind",))
    g3, g4 = st.columns(2)
    g3.slider("Republicans", 0.0, 1.0, step=0.01, format="%.2f",
              key="share_rep", on_change=_rebalance, args=("share_rep",))
    g4.slider("Elites", 0.0, 1.0, step=0.01, format="%.2f",
              key="share_elite", on_change=_rebalance, args=("share_elite",))
    dem_p = st.session_state["share_dem"]
    ind_p = st.session_state["share_ind"]
    rep_p = st.session_state["share_rep"]
    elite_prop = st.session_state["share_elite"]
    st.caption(f"Current mix: {dem_p:.0%} Democrat / {ind_p:.0%} Independent / "
               f"{rep_p:.0%} Republican / {elite_prop:.0%} elite.")
    st.caption("Elites have wider reach and a stronger pull, and don't move when "
               "they talk to ordinary people.")

    st.markdown("**Population size**")
    n_agents = st.slider("Number of people", 100, 1500, 500, step=100)
    st.caption("How many agents in the simulation. Fewer runs faster; the full "
               "dissertation used 5000.")

    st.markdown("**Elite loudness**")
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
    op_initial = result.opinions_history[0]
    op_final = result.opinions_history[-1]
    camp_initial = float(((op_initial < 0.15) | (op_initial > 0.85)).mean())
    camp_final = float(((op_final < 0.15) | (op_final > 0.85)).mean())

    _sigma_help = ("σ, the standard deviation of opinions: ~0 when everyone agrees, "
                   "0.5 when the population splits evenly into two camps at the extremes.")
    _camp_help = ("Share of people at the extremes (opinion below 0.15 or above "
                  "0.85). σ can miss a lopsided split; this number catches it.")

    m1, m2 = st.columns(2)
    m1.metric("Polarization at start", f"{sigma_initial:.2f}", help=_sigma_help)
    m2.metric("Polarization at end", f"{sigma_final:.2f}", f"{sigma_final - sigma_initial:+.2f}",
              help=_sigma_help)
    m3, m4 = st.columns(2)
    m3.metric("At the extremes", f"{camp_final:.0%}", f"{camp_final - camp_initial:+.0%}",
              help=_camp_help)
    m4.metric("Effective tolerance", f"{result.effective_tolerance:.2f}",
              help="T / Gini. Agents within this opinion distance pull together.")

    if camp_final >= 0.5:
        st.markdown("**Result: two hard camps.** Most people have moved to the extremes "
                    "and the middle has emptied out.")
    elif sigma_final <= 0.12 and camp_final <= 0.15:
        st.markdown("**Result: consensus.** The population converged toward the middle.")
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
