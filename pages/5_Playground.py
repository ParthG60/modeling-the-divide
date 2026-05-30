"""Page 5 — Playground: the interactive simulation. Only page that computes live."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from model import DEM, IND, REP, Params, simulate

PARTY_COLOR = {DEM: "#1f77b4", IND: "#888888", REP: "#d62728"}
PARTY_LABEL = {DEM: "Democrat", IND: "Independent", REP: "Republican"}

st.set_page_config(page_title="Playground", layout="wide", page_icon="⚖️")

st.title("Playground")
st.caption("Your turn. Set the dials in the sidebar, hit Run, and watch the divide "
           "form (or not).")

# --- Sidebar controls ----------------------------------------------------------
st.sidebar.title("Parameters")

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
