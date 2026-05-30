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


def fig_initial_distribution():
    """Step-0 distribution split by party — the model's starting assumption."""
    r = simulate(Params(n_agents=600, n_steps=1, seed=42))
    fig, ax = plt.subplots(figsize=(8, 4.2))
    hist_by_party(ax, r.opinions_history[0], r.parties,
                  "Initial opinion distribution (t = 0)", legend=True)
    ax.set_ylabel("Number of agents")
    fig.savefig(FIG / "initial_distribution.png")
    plt.close(fig)
    print("  initial_distribution.png  (initial sigma = %.3f)" % r.polarization[0])


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


def fig_independents_capture():
    """Independents start centered but get pulled into both camps — they don't
    hold the middle. Shows their opinion distribution at start vs end."""
    p = Params(n_agents=600, exposure=0.1, n_steps=600, seed=1)
    r = simulate(p)
    ind = r.parties == IND
    start = r.opinions_history[0][ind]
    end = r.opinions_history[-1][ind]
    mid0 = ((start >= 0.33) & (start <= 0.66)).mean()
    midF = ((end >= 0.33) & (end <= 0.66)).mean()

    fig, ax = plt.subplots(figsize=(8, 4.3))
    ax.hist(start, bins=BINS, color=PARTY_COLOR[IND], alpha=0.35,
            label=f"Start: {mid0*100:.0f}% in the middle")
    ax.hist(end, bins=BINS, color=PARTY_COLOR[IND], alpha=0.9,
            label=f"End: {midF*100:.0f}% in the middle")
    ax.axvspan(0.33, 0.66, color="#94a3b8", alpha=0.12)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Opinion  (0 = left, 1 = right)")
    ax.set_ylabel("Independents")
    ax.set_title("The middle empties: independents get pulled into both camps")
    ax.legend(frameon=False, fontsize=9)
    fig.savefig(FIG / "independents_capture.png")
    plt.close(fig)
    print(f"  independents_capture.png  (middle share {mid0:.2f} -> {midF:.2f})")


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
    ax.plot(vals, sig, "o-", color="#d62728", lw=2, ms=7)
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
    ax.plot(vals, sig, "o-", color="#1f77b4", lw=2, ms=7)
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
    fig_independents_capture()
    fig_sensitivity_exposure()
    fig_sensitivity_gini()
    print("Done.")
