"""Orchestrator agent that coordinates specialized agents."""

from strands import Agent
from strands_tools import file_write
from agents import (
    research_assistant,
    product_recommendation_assistant,
    trip_planning_assistant,
)

# Orchestrator system prompt
MAIN_SYSTEM_PROMPT = """
You are an assistant that routes queries to specialized agents:
- For research questions and factual information → Use the research_assistant tool
- For product recommendations and shopping advice → Use the product_recommendation_assistant tool
- For travel planning and itineraries → Use the trip_planning_assistant tool
- For simple questions not requiring specialized knowledge → Answer directly

Always select the most appropriate tool based on the user's query.
"""


def create_orchestrator() -> Agent:
    """Create and return the orchestrator agent."""
    return Agent(
        model="us.anthropic.claude-sonnet-4-20250514-v1:0",
        system_prompt=MAIN_SYSTEM_PROMPT,
        tools=[
            research_assistant,
            product_recommendation_assistant,
            trip_planning_assistant,
            file_write,
        ],
    )