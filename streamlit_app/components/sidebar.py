"""
Sidebar Component
"""

import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.title("🤖 ML Pipeline")

        st.markdown("---")

        st.success("Project Status")

        st.progress(100)

        st.markdown("### Modules")

        st.write("✅ Data")

        st.write("✅ ML")

        st.write("✅ Monitoring")

        st.write("✅ AI")

        st.write("✅ Self-Healing")

        st.markdown("---")

        st.caption("Version 1.0")