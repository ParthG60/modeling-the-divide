# Modeling the Divide — Interactive Polarization ABM

A narrative-driven Streamlit app built around the agent-based model from my
2024 St Andrews dissertation on political polarization. It walks through *why*
the model is set up the way it is, what it predicts, and how that lines up with
real-world data since 2024 — then hands you the controls.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Structure

Multipage app (`st.navigation` router in `app.py`):

- `app.py` — navigation router (entry point).
- `pages/1_Motivation.py` — the question and the thesis (first-person).
- `pages/2_The_Evidence.py` — current data: OWID polarization score, Pew, Gallup.
- `pages/3_The_Model.py` — the initial setup and why each assumption is made.
- `pages/4_What_Happens.py` — running it forward + the two headline findings.
- `pages/5_Playground.py` — the interactive sim (only page that computes live).
- `pages/6_Methodology.py` — equations and exact rules.

## Other files

- `model.py` — the ABM (initial distributions, interaction probability, 6 influence
  types, Gini-scaled tolerance). Faithful to the dissertation.
- `generate_figures.py` — offline script that pre-renders the static PNGs in
  `figures/` used by the narrative pages (run with `python generate_figures.py`).
- `figures/` — committed static figures (instant load on the narrative pages).
- `requirements.txt` — pinned dependencies.

## Deploy (free public URL)

1. Push to a public GitHub repo.
2. Go to https://share.streamlit.io and connect your GitHub.
3. Point it at `app.py`. Streamlit Community Cloud handles the rest.
