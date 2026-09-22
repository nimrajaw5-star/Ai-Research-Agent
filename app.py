"""
Streamlit front-end for the AI Research Agent.

Type a topic, click a button, and a CrewAI agent will:
1. Search the web using DuckDuckGo (free, no API key needed)
2. Think and write using Groq's `openai/gpt-oss-120b` model
3. Return a Markdown report you can read or download
"""

import streamlit as st

from agent import run_research

st.set_page_config(page_title="AI Research Agent", page_icon="🔎", layout="centered")

st.title("🔎 AI Research Agent")
st.write(
    "Give me a topic, and I'll search the web and write a short report for you.\n\n"
    "Powered by **CrewAI** + **Groq** (`openai/gpt-oss-120b`) + **DuckDuckGo** search."
)

# ---------------------------------------------------------------------------
# Groq API key handling
# ---------------------------------------------------------------------------
# The key is read ONLY from Streamlit secrets. On Streamlit Community Cloud,
# set it under: App settings -> Secrets, as:
#   GROQ_API_KEY = "your_actual_groq_key_here"
groq_api_key = st.secrets.get("GROQ_API_KEY", "")

with st.sidebar:
    st.header("⚙️ About")
    st.caption(
        "This app uses a single CrewAI agent that searches the web with "
        "DuckDuckGo and writes its answer using Groq's `openai/gpt-oss-120b` model."
    )
    if groq_api_key:
        st.success("Groq API key loaded from secrets ✅")
    else:
        st.error(
            "No GROQ_API_KEY found in Streamlit secrets.\n\n"
            "Add it under **App settings → Secrets** as:\n\n"
            '`GROQ_API_KEY = "your_key_here"`'
        )

# ---------------------------------------------------------------------------
# Main input
# ---------------------------------------------------------------------------
topic = st.text_input(
    "Research topic",
    placeholder="e.g. The future of solid-state batteries",
)

run_button = st.button("Run research", type="primary")

if run_button:
    if not groq_api_key:
        st.error(
            "No Groq API key configured. Add GROQ_API_KEY in this app's "
            "Streamlit secrets, then reload the page."
        )
    elif not topic.strip():
        st.error("Please enter a topic to research.")
    else:
        with st.spinner("Researching... this can take a minute or two ⏳"):
            try:
                report = run_research(topic.strip(), groq_api_key.strip())
                st.success("Done! Here's your report:")
                st.markdown(report)
                st.download_button(
                    label="Download report as Markdown",
                    data=report,
                    file_name=f"{topic.strip().replace(' ', '_').lower()}_report.md",
                    mime="text/markdown",
                )
            except Exception as e:
                st.error(f"Something went wrong: {e}")
