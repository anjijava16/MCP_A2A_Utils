"""Root ADK agent for weather lookups."""

from google.adk.agents import Agent

from .tools import weather_search


root_agent = Agent(
    name="weather_agent",
    model="gemini-3-flash-preview",
    instruction=(
        "You are a weather assistant. Use the weather_search tool for current weather questions. "
        "If the user does not provide a city, ask for the city first. If the city may be ambiguous, "
        "ask for a country or region before calling the tool. Keep answers concise and factual."
    ),
    description="Provides current weather information for a requested city.",
    tools=[weather_search],
)
