"""Test script for Bedrock AgentCore travel planning agent."""

import boto3
import json
import uuid
import sys

# Your agent runtime ARN
AGENT_RUNTIME_ARN = "arn:aws:bedrock-agentcore:us-east-1:415529767461:runtime/travel_planning_agent-djIn0T7u1O"

def invoke_agentcore_agent(prompt, agent_runtime_arn=AGENT_RUNTIME_ARN, session_id=None):
    """Invoke an AgentCore agent using the correct API."""
    client = boto3.client('bedrock-agentcore', region_name='us-east-1')
    
    if session_id is None:
        session_id = str(uuid.uuid4())
    
    try:
        print(f"🤔 Sending prompt: {prompt}")
        print(f"📋 Session ID: {session_id}\n")
        
        # Prepare the payload as JSON string
        payload_data = json.dumps({
            "text": prompt
        })
        
        # Use invoke_agent_runtime with the correct parameters
        response = client.invoke_agent_runtime(
            agentRuntimeArn=agent_runtime_arn,
            runtimeSessionId=session_id,  # Changed from sessionId
            payload=payload_data,  # Changed from input
            contentType='application/json'  # Specify content type
        )
        
        print("✅ Response received:")
        
        # The response body is a streaming blob
        if 'body' in response:
            body = response['body'].read()
            
            # Try to parse as JSON
            try:
                response_data = json.loads(body)
                
                # Check for text response
                if isinstance(response_data, dict):
                    if 'text' in response_data:
                        print(response_data['text'])
                    elif 'output' in response_data:
                        print(response_data['output'])
                    else:
                        print(json.dumps(response_data, indent=2))
                else:
                    print(body.decode('utf-8'))
                    
            except json.JSONDecodeError:
                # Not JSON, print as text
                print(body.decode('utf-8'))
        elif 'payload' in response:
            # Handle payload response
            print(response['payload'])
        else:
            # Print entire response structure
            print(json.dumps(response, indent=2, default=str))
        
        print("\n" + "="*70 + "\n")
        
        return {"success": True, "response": response, "session_id": session_id}
        
    except client.exceptions.ResourceNotFoundException as e:
        print(f"❌ Agent not found: {e}")
        return None
    except client.exceptions.ValidationException as e:
        print(f"❌ Validation error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return None

def run_tests(agent_runtime_arn=AGENT_RUNTIME_ARN):
    """Run a series of tests on the travel planning agent."""
    
    print("🤖 Testing Travel Planning Agent (AgentCore)")
    print("=" * 70)
    print(f"Agent ARN: {agent_runtime_arn}")
    print("=" * 70)
    
    # Use the same session for all tests to maintain context
    session_id = str(uuid.uuid4())
    print(f"\n🔗 Using session ID: {session_id}\n")
    
    tests = [
        {
            "name": "Test 1: Greeting",
            "prompt": "Hello! Can you help me plan a trip?"
        },
        {
            "name": "Test 2: Simple destination query",
            "prompt": "What can you tell me about Paris?"
        },
        {
            "name": "Test 3: Trip planning request",
            "prompt": "I want to plan a 5-day trip to Tokyo in March. What should I know?"
        },
        {
            "name": "Test 4: Weather inquiry",
            "prompt": "What's the weather like in London right now?"
        },
        {
            "name": "Test 5: Multi-agent coordination",
            "prompt": "Plan a trip to Rome. I need hotel recommendations and weather information."
        }
    ]
    
    results = []
    
    for test in tests:
        print(f"\n{test['name']}")
        print("-" * 70)
        response = invoke_agentcore_agent(test['prompt'], agent_runtime_arn, session_id=session_id)
        results.append({
            "test": test['name'],
            "success": response is not None and response.get('success', False)
        })
        
        # Small delay between tests
        import time
        time.sleep(1)
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 70)
    for result in results:
        status = "✅ PASSED" if result['success'] else "❌ FAILED"
        print(f"{status}: {result['test']}")
    
    passed = sum(1 for r in results if r['success'])
    print(f"\nTotal: {passed}/{len(results)} tests passed")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Single prompt from command line
        prompt = " ".join(sys.argv[1:])
        invoke_agentcore_agent(prompt)
    else:
        # Run all tests
        run_tests()