# 🔎 AI Research Agent

A beginner-friendly AI research agent built with:

- **[CrewAI](https://www.crewai.com/)** — a single agent that plans and writes the report
- **[Groq](https://groq.com/)** — runs the `openai/gpt-oss-120b` model, super fast and free tier available
- **[DuckDuckGo](https://duckduckgo.com/)** (via the `ddgs` package) — free web search, no API key needed
- **[Streamlit](https://streamlit.io/)** — the web app UI

You type a topic, the agent searches the web a few times, and it writes you a
Markdown report with sources. The Groq API key is read **only from Streamlit
secrets** — there's no key field in the app itself.

---

## 📁 Project structure

```
ai-research-agent/
├── app.py              # Streamlit UI — reads GROQ_API_KEY from st.secrets
├── agent.py            # Defines the CrewAI Agent, Task and Crew
├── tools.py            # The DuckDuckGo search tool the agent uses
├── requirements.txt    # Python dependencies
├── .gitignore          # Keeps secrets and junk out of GitHub
└── README.md           # You are here
```

---

## 1. Get a free Groq API key

1. Go to <https://console.groq.com/keys>
2. Sign up (it's free) and create a new API key
3. Copy it somewhere safe — you'll paste it into Streamlit's secrets in step 3

---

## 2. Upload this project to GitHub

1. Go to <https://github.com/new> and create a new **empty** repository
   (don't add a README, .gitignore, or license there — you already have them).
2. Open your new repo, click **"Add file" → "Upload files"**.
3. Drag in all the files from this project: `app.py`, `agent.py`, `tools.py`,
   `requirements.txt`, `.gitignore`, and `README.md`.
4. Scroll down and click **"Commit changes"**.

That's it — no `git` commands needed.

---

## 3. Deploy on Streamlit Community Cloud

1. Go to <https://share.streamlit.io/> and sign in with GitHub.
2. Click **"New app"**.
3. Pick your repository, branch (`main`), and set the main file path to
   `app.py`.
4. Before clicking Deploy, open **"Advanced settings" → "Secrets"** and add:

   ```toml
   GROQ_API_KEY = "your_actual_groq_key_here"
   ```

   This keeps your key private and out of your GitHub repo. `app.py` reads
   it automatically via `st.secrets["GROQ_API_KEY"]` — no other setup needed.

5. Click **Deploy**. The first build can take a couple of minutes while it
   installs everything from `requirements.txt`.
6. Once it's live, open the app — the sidebar should show
   **"Groq API key loaded from secrets ✅"**. If it instead shows an error,
   double-check the secret's exact name (`GROQ_API_KEY`) and that it's saved.

### Updating your secret later

If you ever need to change the key: go to your app on
<https://share.streamlit.io/>, click the **⋮ menu → Settings → Secrets**,
edit the value, save, and the app will reboot automatically.

---

## How it works (quick tour for beginners)

- **`tools.py`** wraps the `ddgs` library into a CrewAI "tool" — basically a
  Python function the agent is allowed to call, with a docstring that tells
  the agent *when* and *how* to use it. The agent decides on its own how
  many times to call it and with what search queries.

- **`agent.py`** creates:
  - one `Agent` (the "Senior Research Analyst") with a role, goal, and the
    search tool attached,
  - one `Task` describing exactly what the output report should look like,
  - one `Crew` that ties them together and runs the task with
    `Process.sequential` (the simplest way to run a crew — the agent just
    completes its one task from start to finish).

- **`app.py`** is a normal Streamlit script: it reads the Groq key from
  `st.secrets`, shows a text box for the topic, and calls `run_research()`
  from `agent.py` to display the Markdown result.

---

## Troubleshooting

- **Sidebar shows "No GROQ_API_KEY found in Streamlit secrets"** — go to
  your app's Settings → Secrets on Streamlit Cloud and make sure the key is
  named exactly `GROQ_API_KEY` and the value is wrapped in quotes.
- **App is slow / times out** — the free Groq tier has rate limits; try a
  narrower topic, or wait a few seconds and try again.
- **`ModuleNotFoundError` during deploy** — check `requirements.txt` was
  uploaded correctly and that the app's main file path is set to `app.py`.
- **Search returns no results** — DuckDuckGo occasionally rate-limits
  requests from cloud servers; wait a bit and try again, or rephrase the
  topic.

---

## Ideas to extend this project once you're comfortable

- Add a second agent (e.g. a "Fact Checker") and turn this into a real
  multi-agent crew.
- Let the user pick the number of sources or the report length.
- Swap in a different Groq model (see <https://console.groq.com/docs/models>)
  by changing the `model=` string in `agent.py`.
- Cache reports so the same topic isn't researched twice.
