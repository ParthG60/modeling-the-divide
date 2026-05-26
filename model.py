"""
Agent-Based Model of political polarization.

Faithful re-implementation of the model from Goyal (2024),
"Modeling the Divide: Mathematical Approaches to Understanding and Mitigating
Political Polarization", University of St Andrews.

Core equations:
- Initial opinion distribution: Eq. 2.1 (group-specific normals on [0,1])
- Interaction probability:        Eq. 2.2  p = (1/2)^(d/E)  (× prob_multiplier if elite)
- Opinion update:                 Eq. 2.3  six influence types
- Effective tolerance:            Eq. 2.4  Tolerance = T / Gini

Interaction types from Table 2.2:
  Strong positive   : same-party (Elite + Mass)
  Regular positive  : same-party same-status / both Independents within tol /
                      different-party (Elite + Mass) within tol /
                      Partisan-Elite + Independent-Mass within tol
  Weak positive     : same-status different-party within tol
  Strong negative   : different-party (Elite + Mass) outside tol
  Regular negative  : different-party same-status outside tol /
                      Partisan-Elite + Independent-Mass outside tol
  Weak negative     : both Independents outside tol

Implementation notes:
- Each step, every agent picks one random partner (instead of all O(N^2) pairs).
  This keeps the demo interactive while preserving the model's stochastic
  pairwise dynamics. With sufficient steps the same equilibria emerge.
- Updates are applied sequentially in shuffled order within a step.
- Elites do not move when interacting with masses (asymmetric update).
"""

from dataclasses import dataclass, field
import numpy as np

# Party encoding
DEM = 0
IND = 1
REP = 2

PARTY_NAMES = {DEM: "Democrat", IND: "Independent", REP: "Republican"}


@dataclass
class Params:
    # Population
    n_agents: int = 500
    dem_proportion: float = 0.331
    ind_proportion: float = 0.338
    rep_proportion: float = 0.331
    elite_proportion: float = 0.05   # dissertation used ~0.5%; bump for demo visibility
    # Core parameters
    exposure: float = 0.1            # E
    tolerance: float = 0.1           # T  (effective tol = T / Gini)
    responsiveness: float = 0.25     # R
    gini: float = 0.434
    impact_multiplier: float = 1.2
    prob_multiplier: float = 1.2
    # Simulation
    n_steps: int = 300
    seed: int = 42


@dataclass
class SimResult:
    opinions_history: np.ndarray  # (n_steps+1, n_agents)
    parties: np.ndarray           # (n_agents,)
    is_elite: np.ndarray          # (n_agents,)
    params: Params = field(default=None)

    @property
    def polarization(self) -> np.ndarray:
        """Std dev of opinions at each step — the dissertation's polarization measure."""
        return self.opinions_history.std(axis=1)

    @property
    def effective_tolerance(self) -> float:
        return self.params.tolerance / self.params.gini


def init_agents(p: Params, rng: np.random.Generator):
    N = p.n_agents
    # Normalize party proportions
    props = np.array([p.dem_proportion, p.ind_proportion, p.rep_proportion])
    props = props / props.sum()
    parties = rng.choice([DEM, IND, REP], size=N, p=props)
    is_elite = rng.random(N) < p.elite_proportion

    opinions = np.empty(N)
    # Dissertation Eq. 2.1
    for i in range(N):
        party, elite = parties[i], is_elite[i]
        if party == IND:
            mu, sigma = 0.5, 0.2
        elif party == DEM:
            mu, sigma = 0.35, (0.2 if elite else 0.15)
        else:  # REP
            mu, sigma = 0.65, (0.2 if elite else 0.15)
        opinions[i] = rng.normal(mu, sigma)

    np.clip(opinions, 0.0, 1.0, out=opinions)
    return opinions, parties, is_elite


def classify_influence(party_i, party_j, elite_i, elite_j, within_tol):
    """
    Return (sign, strength) for the pair, following Table 2.2.
      sign:    +1 attract, -1 repel
      strength: 'strong', 'regular', 'weak'
    """
    same_party = party_i == party_j
    both_ind = party_i == IND and party_j == IND
    one_ind = (party_i == IND) ^ (party_j == IND)
    both_partisan_diff = (party_i != IND) and (party_j != IND) and (party_i != party_j)
    elite_mass = elite_i != elite_j
    same_status = elite_i == elite_j

    # Same-party partisans: always attract (tribalism — bypass tolerance)
    if same_party and party_i != IND:
        return (+1, "strong" if elite_mass else "regular")

    # Both independents
    if both_ind:
        if same_status and within_tol:
            return (+1, "regular")
        return (-1, "weak")

    # Different-party partisans
    if both_partisan_diff:
        if elite_mass:
            return (+1, "regular") if within_tol else (-1, "strong")
        # same status
        return (+1, "weak") if within_tol else (-1, "regular")

    # Mixed: partisan + independent
    if one_ind:
        # Dissertation explicitly names Partisan-Elite + Independent-Mass cases.
        # For other partisan-independent pairs, use the same regular-positive /
        # regular-negative rule by symmetry.
        return (+1, "regular") if within_tol else (-1, "regular")

    return (0, "regular")


def step(opinions, parties, is_elite, p: Params, rng: np.random.Generator):
    """One timestep: each agent picks a random partner, sequential updates."""
    N = len(opinions)
    eff_tol = p.tolerance / p.gini

    # Each agent's partner (avoid self)
    partners = rng.integers(0, N, size=N)
    self_mask = partners == np.arange(N)
    partners[self_mask] = (partners[self_mask] + 1) % N

    # Random update order
    order = rng.permutation(N)

    for i in order:
        j = partners[i]
        d = abs(opinions[i] - opinions[j])

        # Eq. 2.2 — interaction probability
        prob = 0.5 ** (d / max(p.exposure, 1e-6))
        if is_elite[i] or is_elite[j]:
            prob *= p.prob_multiplier
        if rng.random() > min(prob, 1.0):
            continue

        sign, strength = classify_influence(
            parties[i], parties[j], is_elite[i], is_elite[j], within_tol=(d <= eff_tol)
        )
        if sign == 0:
            continue

        # Eq. 2.3 — opinion update
        base = p.responsiveness * (opinions[j] - opinions[i])
        if strength == "strong":
            delta = base * p.impact_multiplier
        elif strength == "weak":
            delta = base / p.impact_multiplier
        else:
            delta = base

        # Elite ignores mass: only mass agent (i.e. non-elite in mixed pair) updates
        if is_elite[i] and not is_elite[j]:
            continue  # i is elite, j is mass — i stays put, j updates when it's j's turn
        opinions[i] = np.clip(opinions[i] + sign * delta, 0.0, 1.0)


def simulate(p: Params) -> SimResult:
    rng = np.random.default_rng(p.seed)
    opinions, parties, is_elite = init_agents(p, rng)

    history = np.empty((p.n_steps + 1, p.n_agents), dtype=np.float32)
    history[0] = opinions

    for t in range(1, p.n_steps + 1):
        step(opinions, parties, is_elite, p, rng)
        history[t] = opinions

    return SimResult(
        opinions_history=history,
        parties=parties,
        is_elite=is_elite,
        params=p,
    )
