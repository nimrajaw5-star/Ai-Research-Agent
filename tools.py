"""
A custom tool that lets our CrewAI agent search the web using DuckDuckGo.

Why a custom tool instead of an existing one?
- DuckDuckGo needs NO API key, so it's the easiest free search option
  for a beginner project.
- The `ddgs` package (the modern, maintained version of the old
  `duckduckgo_search` package) gives us search results directly, without
  needing extra libraries like langchain.
"""

from crewai.tools import tool
from ddgs import DDGS


@tool("DuckDuckGo Search")
def duckduckgo_search(query: str) -> str:
    """
    Searches the web using DuckDuckGo and returns the top results
    (title, link, and a short snippet for each).

    Use this tool whenever you need up-to-date facts, articles, or
    sources about the research topic you were given. You can call it
    more than once with different search queries to cover the topic
    from different angles.

    Args:
        query: The search query (keywords) to look up on the web.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=6))

        if not results:
            return f"No search results found for '{query}'. Try a different query."

        formatted_results = []
        for i, r in enumerate(results, start=1):
            title = r.get("title", "No title")
            link = r.get("href", "No link")
            snippet = r.get("body", "No description available")
            formatted_results.append(
                f"{i}. {title}\n   Link: {link}\n   Snippet: {snippet}"
            )

        return "\n\n".join(formatted_results)

    except Exception as e:
        return f"Search failed for query '{query}'. Error: {e}"
