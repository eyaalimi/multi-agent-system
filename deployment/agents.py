"""Specialized agent tools for the travel planning system."""

from strands import Agent, tool

# System prompts
RESEARCH_ASSISTANT_PROMPT = """You are a specialized research assistant. Focus only on providing
factual, well-sourced information in response to research questions.
Always cite your sources when possible."""


@tool
def research_assistant(query: str) -> str:
    """
    Process and respond to research-related queries about destinations, cultures, and travel information.

    Args:
        query: A research question requiring factual information

    Returns:
        A detailed research answer with citations
    """
    try:
        research_agent = Agent(
            model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            system_prompt=RESEARCH_ASSISTANT_PROMPT,
        )
        response = research_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in research assistant: {str(e)}"


@tool
def product_recommendation_assistant(query: str) -> str:
    """
    Handle travel product recommendation queries by suggesting appropriate gear and equipment.

    Args:
        query: A product inquiry with user preferences and travel needs

    Returns:
        Personalized product recommendations with reasoning
    """
    try:
        product_agent = Agent(
            model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            system_prompt="""You are a specialized travel product recommendation assistant.
            Provide personalized product suggestions for travelers based on their destination, 
            activities, and preferences. Focus on quality, durability, and value. 
            Always cite your sources when possible.""",
        )
        response = product_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in product recommendation: {str(e)}"


@tool
def trip_planning_assistant(query: str) -> str:
    """
    Create detailed travel itineraries and provide comprehensive travel planning advice.

    Args:
        query: A travel planning request with destination, duration, and preferences

    Returns:
        A detailed travel itinerary with day-by-day plans and recommendations
    """
    try:
        travel_agent = Agent(
            model="us.anthropic.claude-sonnet-4-20250514-v1:0",
            system_prompt="""You are a specialized travel planning assistant.
            Create detailed, practical travel itineraries based on user preferences.
            Include accommodation suggestions, transportation options, activity recommendations,
            timing details, and budget considerations. Provide realistic daily schedules
            and highlight must-see attractions as well as hidden gems.""",
        )
        response = travel_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in trip planning: {str(e)}"