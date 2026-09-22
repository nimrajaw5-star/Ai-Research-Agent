"""
Defines our single research Agent, its Task, and the Crew that runs them.

This is intentionally a ONE-agent crew:
- One Agent  -> "Senior Research Analyst"
- One Task   -> "Research the topic and write a report"
- One Crew   -> runs that single task

Keeping it to a single agent/task keeps things simple to understand and
cheap/fast to run, which is perfect while you're learning CrewAI.
"""

import os

from crewai import Agent, Task, Crew, Process, LLM

from tools import duckduckgo_search


# -----------------------------------------------------------------------
# Compatibility patch (safe to keep even after CrewAI fixes this upstream)
# -----------------------------------------------------------------------
# Some CrewAI/LiteLLM versions tag every outgoing message with an
# Anthropic-only "cache_breakpoint" marker used for prompt caching. Groq's
# API doesn't recognize that field and rejects the whole request with:
#   GroqException - property 'cache_breakpoint' is unsupported
#
# This wraps LiteLLM's actual request functions and strips that one key
# from messages right before they go out over the network, no matter which
# internal CrewAI code path added it. It's a no-op for any message that
# doesn't have the key, so it's safe for other providers too.
# Background: https://github.com/crewAIInc/crewAI/issues/5886
def _patch_litellm_cache_breakpoint() -> None:
    try:
        import litellm
    except ImportError:
        return

    def _strip(messages):
        if not messages:
            return messages
        return [
            {k: v for k, v in m.items() if k != "cache_breakpoint"}
            if isinstance(m, dict)
            else m
            for m in messages
        ]

    original_completion = getattr(litellm, "completion", None)
    if original_completion and not getattr(original_completion, "_cache_breakpoint_patched", False):
        def patched_completion(*args, **kwargs):
            if "messages" in kwargs:
                kwargs["messages"] = _strip(kwargs["messages"])
            return original_completion(*args, **kwargs)

        patched_completion._cache_breakpoint_patched = True
        litellm.completion = patched_completion

    original_acompletion = getattr(litellm, "acompletion", None)
    if original_acompletion and not getattr(original_acompletion, "_cache_breakpoint_patched", False):
        async def patched_acompletion(*args, **kwargs):
            if "messages" in kwargs:
                kwargs["messages"] = _strip(kwargs["messages"])
            return await original_acompletion(*args, **kwargs)

        patched_acompletion._cache_breakpoint_patched = True
        litellm.acompletion = patched_acompletion


_patch_litellm_cache_breakpoint()


def build_crew(topic: str, groq_api_key: str) -> Crew:
    """Builds (but does not run) the Crew for a given research topic."""

    # CrewAI/LiteLLM look for the Groq key in this exact environment variable.
    os.environ["GROQ_API_KEY"] = groq_api_key

    # The "groq/" prefix tells CrewAI which provider to route the request to.
    # "openai/gpt-oss-120b" is the actual model name Groq hosts.
    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        temperature=0.4,
    )

    researcher = Agent(
        role="Senior Research Analyst",
        goal=(
            f"Research the topic '{topic}' thoroughly using web search, "
            "then write a clear, well-organized report on it."
        ),
        backstory=(
            "You are an experienced research analyst known for turning "
            "messy web search results into clear, trustworthy reports. "
            "You always check information from a few different searches "
            "before drawing conclusions, and you write in plain language "
            "that a general audience can easily follow."
        ),
        tools=[duckduckgo_search],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    research_task = Task(
        description=(
            f"Research the following topic: '{topic}'.\n\n"
            "Follow these steps:\n"
            "1. Use the DuckDuckGo Search tool with two or three different "
            "search queries to gather up-to-date information on the topic.\n"
            "2. Read through the results and identify the key facts, "
            "different viewpoints, and any recent developments.\n"
            "3. Write a final report based ONLY on what you actually found "
            "in the search results. Do not make up facts or sources.\n\n"
            "The final report must include:\n"
            "- A short introduction to the topic\n"
            "- 3 to 6 main sections, each with a clear Markdown heading, "
            "covering the key findings\n"
            "- A short conclusion summarizing the main takeaways\n"
            "- A 'Sources' section at the end, listing the links you used\n"
        ),
        expected_output=(
            "A well-structured report written in Markdown, with clear "
            "headings, short readable paragraphs, and a final list of "
            "source links."
        ),
        agent=researcher,
    )

    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True,
    )

    return crew


def run_research(topic: str, groq_api_key: str) -> str:
    """Builds the crew and runs it, returning the final report as text."""
    crew = build_crew(topic, groq_api_key)
    result = crew.kickoff()
    return str(result)


def run_research(topic: str, groq_api_key: str) -> str:
    """Builds the crew and runs it, returning the final report as text."""
    crew = build_crew(topic, groq_api_key)
    result = crew.kickoff()
    return str(result)
