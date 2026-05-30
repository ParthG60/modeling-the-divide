"""
Modeling the Divide — interactive companion to my 2024 St Andrews dissertation
on agent-based modeling of political polarization.

This is the entry point: a navigation router. The walkthrough lives in pages/.
Each page sets its own page config (so Playground can be wide while the narrative
pages stay centered), so we deliberately do NOT call st.set_page_config here.

Run locally:  streamlit run app.py
"""

import streamlit as st

pages = [
    st.Page("pages/1_Motivation.py",   title="Start here",     icon="🏠", default=True),
    st.Page("pages/2_The_Evidence.py", title="The Evidence",   icon="📊"),
    st.Page("pages/3_The_Model.py",    title="The Model",      icon="⚙️"),
    st.Page("pages/4_What_Happens.py", title="What Happens",   icon="📈"),
    st.Page("pages/5_Playground.py",   title="Playground",     icon="🎛️"),
    st.Page("pages/6_Methodology.py",  title="Methodology",    icon="📐"),
]

st.navigation(pages).run()
