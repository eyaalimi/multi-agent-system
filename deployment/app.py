"""Travel Assistant Agent for Amazon Bedrock AgentCore Runtime."""

from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

# Import your specialized agent tools
from agents import (
    research_assistant,
    product_recommendation_assistant,
    trip_planning_assistant,
)

# Import Strands built-in tools
from strands_tools import current_time

import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize AgentCore app
app = BedrockAgentCoreApp()

# System prompt for the travel orchestrator
ORCHESTRATOR_SYSTEM_PROMPT = """
You are a Travel Planning Orchestrator that helps users plan trips and find travel-related products.
You coordinate with specialized assistants to provide comprehensive travel planning services.

You have access to three specialized assistants:
- **Research Assistant**: For factual information about destinations, cultures, attractions, and travel tips
- **Product Recommendation Assistant**: For travel gear, equipment, and product recommendations
- **Trip Planning Assistant**: For creating detailed itineraries and travel plans

Guidelines:
1. Analyze the user's request carefully
2. Route queries to the most appropriate specialist(s)
3. For complex requests, coordinate multiple specialists
4. Always provide helpful, accurate, and personalized recommendations
5. Be friendly and professional in all interactions
6. If you cannot answer a question, politely explain your limitations

When planning trips:
- Consider budget, duration, and traveler preferences
- Suggest practical itineraries with timing details
- Include accommodation, transportation, and activity recommendations
- Highlight must-see attractions and hidden gems

When recommending products:
- Match recommendations to the specific trip and activities
- Consider quality, durability, and value
- Provide multiple options when possible

Always maintain context across the conversation to provide a seamless experience.
"""

# Create the Strands orchestrator agent
model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    additional_request_fields={"thinking": {"type": "disabled"}}
)

orchestrator = Agent(
    model=model,
    tools=[
        research_assistant,
        product_recommendation_assistant,
        trip_planning_assistant,
        current_time,
    ],
    system_prompt=ORCHESTRATOR_SYSTEM_PROMPT
)

@app.entrypoint
def invoke(payload, context):
    """
    Main entry point for AgentCore Runtime invocations.
    
    Args:
        payload: Request data containing the user's prompt
        context: Session context with session_id for state management
        
    Returns:
        str: Agent response
    """
    prompt = payload.get("prompt", "Hello! How can I help you plan your trip?")
    session_id = context.session_id if context else None
    
    logger.info(f"Processing request - Session: {session_id}")
    logger.info(f"User prompt: {prompt}")
    
    try:
        # Invoke the orchestrator agent
        response = orchestrator(prompt)
        
        # Extract the text response
        result = response.message['content'][0]['text']
        
        logger.info(f"Response generated successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return f"I apologize, but I encountered an error while processing your request. Please try again or rephrase your question."

if __name__ == "__main__":
    app.run()