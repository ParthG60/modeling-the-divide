"""
Pre-render the static figures used in the narrative walkthrough.
Run offline once (and whenever the model changes):  python generate_figures.py
Outputs PNGs into figures/ which are committed and served by the app.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from model import DEM, IND, REP, Params, simulate

FIG = Path(__file__).parent / "figures"
FIG.mkdir(exist_ok=True)

PARTY_COLOR = {DEM: "#2563eb", IND: "#7c3aed", REP: "#dc2626"}
PARTY_LABEL = {DEM: "Democrat", IND: "Independent", REP: "Republican"}
BINS = np.linspace(0, 1, 41)

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.dpi": 110,
    "savefig.bbox": "tight",
})


def hist_by_party(ax, opinions, parties, title, legend=False):
    for party in [DEM, IND, REP]:
        mask = parties == party
        if mask.sum() == 0:
            continue
        ax.hist(opinions[mask], bins=BINS, color=PARTY_COLOR[party],
                alpha=0.7, label=PARTY_LABEL[party])
    ax.set_xlim(0, 1)
    ax.set_xlabel("Opinion  (0 = left, 1 = right)")
    ax.set_title(title)
    if legend:
        ax.legend(frameon=False, fontsize=9)


def _kde(data, grid, bw):
    """Gaussian kernel density estimate (numpy-only)."""
    u = (grid[:, None] - data[None, :]) / bw
    return np.exp(-0.5 * u * u).sum(axis=1) / (len(data) * bw * np.sqrt(2 * np.pi))


def fig_initial_distribution():
    """Step-0 distribution split by party, drawn as smooth density curves.
    Large N (matching the dissertation) for a clean estimate."""
    r = simulate(Params(n_agents=5000, n_steps=1, seed=42))
    grid = np.linspace(0, 1, 400)
    N = len(r.parties)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for party in [DEM, IND, REP]:
        d = r.opinions_history[0][r.parties == party]
        iqr = np.subtract(*np.percentile(d, [75, 25]))
        bw = 0.9 * min(d.std(), iqr / 1.34) * len(d) ** (-0.2)  # Silverman
        dens = _kde(d, grid, bw) * (len(d) / N)  # scale by population share
        ax.fill_between(grid, dens, color=PARTY_COLOR[party], alpha=0.45)
        ax.plot(grid, dens, color=PARTY_COLOR[party], lw=2, label=PARTY_LABEL[party])
    ax.set_xlim(0, 1)
    ax.set_ylim(bottom=0)
    ax.set_yticks([])
    ax.set_xlabel("Opinion  (0 = left, 1 = right)")
    ax.set_ylabel("Share of agents")
    ax.set_title("Initial opinion distribution (t = 0)")
    ax.legend(frameon=False, fontsize=9)
    fig.savefig(FIG / "initial_distribution.png")
    plt.close(fig)
    print("  initial_distribution.png  (smooth KDE, sigma = %.3f)" % r.polarization[0])


def fig_evolution_panel():
    """One canonical run (base case E=0.1) shown at start / midway / polarized."""
    p = Params(n_agents=600, exposure=0.1, n_steps=600, seed=1)
    r = simulate(p)
    steps = [0, 150, 600]
    titles = ["Start (t = 0)", "Forming camps (t = 150)", "Two camps (t = 600)"]
    fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
    for ax, t, title in zip(axes, steps, titles):
        sigma = r.opinions_history[t].std()
        hist_by_party(ax, r.opinions_history[t], r.parties,
                      f"{title}\nσ = {sigma:.2f}", legend=(t == 0))
    axes[0].set_ylabel("Number of agents")
    fig.suptitle("Running the base case forward: a centred population splits in two",
                 fontsize=13, y=1.04)
    fig.savefig(FIG / "evolution_panel.png")
    plt.close(fig)
    print("  evolution_panel.png  (sigma: %.3f -> %.3f)"
          % (r.polarization[0], r.polarization[-1]))


def fig_independents_dampen(seeds=range(10)):
    """More independents in the population -> lower final polarization.
    Averages final sigma over seeds for a range of independent shares."""
    shares = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    means, sds = [], []
    for ind in shares:
        finals = []
        for s in seeds:
            dem = rep = (1 - ind) / 2
            p = Params(n_agents=500, dem_proportion=dem, ind_proportion=ind,
                       rep_proportion=rep, exposure=0.1, tolerance=0.1,
                       gini=0.434, n_steps=500, seed=s)
            finals.append(simulate(p).polarization[-1])
        means.append(np.mean(finals)); sds.append(np.std(finals))
    means, sds = np.array(means), np.array(sds)

    fig, ax = plt.subplots(figsize=(7.5, 4.3))
    ax.fill_between(shares, means - sds, means + sds, color="#0f766e", alpha=0.15)
    ax.plot(shares, means, "o-", color="#0f766e", lw=2.5, ms=7)
    ax.axvline(0.34, color="#888", ls="--", lw=1)
    ax.text(0.345, 0.07, "US (~34%)", fontsize=8, color="#555")
    ax.set_xlabel("Independents' share of the population")
    ax.set_ylabel("Final polarization  (σ of opinions)")
    ax.set_title("More independents, less polarization")
    ax.set_ylim(0, 0.5)
    ax.grid(alpha=0.25)
    fig.savefig(FIG / "independents_dampen.png")
    plt.close(fig)
    print(f"  independents_dampen.png  sigma: {np.round(means, 3)}")


def sweep(param_name, values, base=None, n_steps=400, seeds=(0, 1, 2, 3, 4)):
    """Average final polarization (sigma) over seeds for each value."""
    base = base or {}
    out = []
    for v in values:
        finals = []
        for s in seeds:
            kwargs = dict(n_agents=500, n_steps=n_steps, seed=s, **base)
            kwargs[param_name] = v
            r = simulate(Params(**kwargs))
            finals.append(r.polarization[-1])
        out.append(np.mean(finals))
    return np.array(out)


def fig_sensitivity_exposure():
    vals = [0.05, 0.1, 0.2, 0.4, 0.8]
    sig = sweep("exposure", vals)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(vals, sig, "o-", color="#0f766e", lw=2.5, ms=7)
    ax.set_xlabel("Exposure (E)")
    ax.set_ylabel("Final polarization  (σ of opinions)")
    ax.set_title("More exposure → more polarization")
    ax.set_ylim(0, 0.55)
    ax.grid(alpha=0.25)
    fig.savefig(FIG / "sensitivity_exposure.png")
    plt.close(fig)
    print("  sensitivity_exposure.png  sigma:", np.round(sig, 3))


def fig_sensitivity_gini():
    vals = [0.25, 0.35, 0.434, 0.55, 0.7]
    sig = sweep("gini", vals)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(vals, sig, "o-", color="#0f766e", lw=2.5, ms=7)
    ax.axvline(0.434, color="#888", ls="--", lw=1)
    ax.text(0.44, 0.02, "US base case\n(Gini = 0.434)", fontsize=8, color="#555")
    ax.set_xlabel("Gini coefficient (economic inequality)")
    ax.set_ylabel("Final polarization  (σ of opinions)")
    ax.set_title("More inequality → less tolerance → more polarization")
    ax.set_ylim(0, 0.55)
    ax.grid(alpha=0.25)
    fig.savefig(FIG / "sensitivity_gini.png")
    plt.close(fig)
    print("  sensitivity_gini.png  sigma:", np.round(sig, 3))


if __name__ == "__main__":
    print("Generating figures into", FIG)
    fig_initial_distribution()
    fig_evolution_panel()
    fig_independents_dampen()
    fig_sensitivity_exposure()
    fig_sensitivity_gini()
    print("Done.")
