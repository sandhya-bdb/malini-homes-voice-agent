import sys

print("Loading configuration and agent modules...", flush=True)
from config import settings
from langchain_agent import malini_agent

print("--- Testing Malini Voice Agent ---", flush=True)
try:
    print("Invoking agent query...", flush=True)
    response = malini_agent.invoke({
        "messages": [("user", "Hello! What rooms are available in Silpukhuri and what are the rates?")]
    })
    for m in response["messages"]:
        if hasattr(m, "content") and m.content and m.type == "ai":
            print(f"\n[AI Response]:\n{m.content}", flush=True)
except Exception as e:
    print(f"Error during invocation: {e}", flush=True)
    sys.exit(1)
print("\n[SUCCESS] Agent test completed successfully!", flush=True)

