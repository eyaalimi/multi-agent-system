"""Interactive multi-agent system - Ask anything!"""

import os
from orchestrator import create_orchestrator


def main():
    """Run interactive multi-agent system."""
    
    # Bypass tool consent for automation
    os.environ["BYPASS_TOOL_CONSENT"] = "true"
    
    # Create the orchestrator
    print("🤖 Multi-Agent System Starting...")
    print("="*70)
    orchestrator = create_orchestrator()
    print("✅ System Ready! Available agents:")
    print("   📚 Research Assistant")
    print("   🛒 Product Recommendation Assistant")
    print("   ✈️  Trip Planning Assistant")
    print("="*70)
    print("\nType your question (or 'quit' to exit, 'clear' to reset conversation)\n")
    
    while True:
        # Get user input
        try:
            query = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Goodbye!")
            break
        
        # Handle special commands
        if query.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if query.lower() == 'clear':
            orchestrator.messages = []
            print("🧹 Conversation cleared!\n")
            continue
        
        if query.lower() == 'help':
            print("\n📖 Available commands:")
            print("   - Type any question to ask the agents")
            print("   - 'clear' - Reset conversation history")
            print("   - 'quit' or 'exit' - Exit the program")
            print("   - 'help' - Show this message\n")
            continue
        
        if not query:
            continue
        
        # Process query
        print(f"\n🤔 Processing...\n")
        try:
            response = orchestrator(query)
            print(f"🤖 Agent: {response}\n")
            print("-"*70 + "\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()