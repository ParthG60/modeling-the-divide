# Polarization ABM — Interactive App

Streamlit app that lets anyone play with the agent-based polarization model
from my 2024 St Andrews dissertation.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

App opens at http://localhost:8501.

## Deploy (free public URL)

1. Push this folder to a public GitHub repo (it can be a subfolder of a larger repo).
2. Go to https://share.streamlit.io and connect your GitHub.
3. Point it at `app.py` in this folder. Streamlit Community Cloud handles the rest.
4. You get a public URL like `https://yourname-polarization-abm.streamlit.app`
   that you can link to from anywhere.

## Files

- `model.py` — core ABM (initial distributions, interaction probability,
  6 influence types, Gini-scaled tolerance). Faithful to the dissertation.
- `app.py` — Streamlit UI: sliders, plots, methodology tab.
- `requirements.txt` — pinned-loose dependencies.
