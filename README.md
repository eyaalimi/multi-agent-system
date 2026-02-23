# 🤖 Multi-Agent System with Orchestrator Pattern

A Python-based multi-agent AI system using the Strands framework, implementing the "Agents as Tools" architectural pattern. This system intelligently routes user queries to specialized AI agents for research, product recommendations, and trip planning.

## 🏗️ Architecture
                    User Query
                        ↓
              Orchestrator Agent
              (Intelligent Router)
                        ↓
        ┌───────────────┼───────────────┐
        ↓               ↓               ↓
📚 Research      🛒 Product      ✈️ Trip
 Assistant      Assistant        Planner



 
### How It Works

The orchestrator analyzes each query and delegates to the most appropriate specialist:
- **Research questions** → Research Assistant (factual information, citations)
- **Product inquiries** → Product Recommendation Assistant (personalized suggestions)
- **Travel requests** → Trip Planning Assistant (itineraries, travel advice)
- **Complex queries** → Multiple agents working in sequence

## ✨ Features

- **🎯 Intelligent Routing**: Automatically selects the right specialist for each task
- **🔧 Modular Design**: Easy to add, remove, or modify specialist agents
- **💬 Interactive CLI**: Natural conversation interface
- **🔗 Sequential Workflows**: Agents can pass information to each other
- **🛠️ Extensible**: Built on the Strands framework for easy customization
- **📝 File Operations**: Can write results to files using built-in tools

## 📦 Installation

### Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- AWS credentials configured

### Setup Steps

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/multi-agent-system.git
cd multi-agent-system

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
