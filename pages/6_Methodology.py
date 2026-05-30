"""Page 6 — Methodology: the equations and exact rules."""

import streamlit as st

st.set_page_config(page_title="Methodology", layout="centered", page_icon="⚖️")

st.title("Methodology")

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
