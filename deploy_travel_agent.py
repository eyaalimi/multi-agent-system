"""Deploy travel planning agent to AWS AgentCore Runtime."""

import boto3
import time
import sys

sys.path.insert(0, './deployment')

from bedrock_agentcore_starter_toolkit import Runtime
from deployment.utils import create_execution_role

# Configuration
agent_name = "travel_planning_agent"
session = boto3.Session()
region = session.region_name or "us-east-1"
account_id = boto3.client("sts").get_caller_identity()["Account"]

print(f"🌍 Region: {region}")
print(f"🔑 Account: {account_id}\n")

# Create execution role
print("📝 Creating execution role...")
execution_role_arn, role_name = create_execution_role(agent_name)
print(f"✅ Role created: {execution_role_arn}\n")

# Configure runtime
print("⚙️  Configuring AgentCore Runtime...")
runtime = Runtime()
config = runtime.configure(
    entrypoint="deployment/app.py",
    execution_role=execution_role_arn,
    auto_create_ecr=True,
    requirements_file="deployment/requirements.txt",
    region=region,
    agent_name=agent_name
)
print("✅ Configuration complete\n")

# Deploy
print("🚀 Deploying agent...")
print("This may take several minutes...\n")
launch = runtime.launch()

# Wait for deployment
status_obj = runtime.status()
status = status_obj.endpoint["status"]
terminal_states = {"READY", "CREATE_FAILED", "DELETE_FAILED", "UPDATE_FAILED"}

while status not in terminal_states:
    print(f"📊 Status: {status}")
    time.sleep(10)
    status_obj = runtime.status()
    status = status_obj.endpoint["status"]

print(f"\n🎉 Final Status: {status}")

if status == "READY":
    print("✅ Agent is ready!")
    print("\nTest it with:")
    print(f'  runtime.invoke({{"prompt": "Plan a trip to Paris"}})')
else:
    print("❌ Deployment failed. Check CloudWatch logs.")