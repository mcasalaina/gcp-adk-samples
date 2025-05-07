import os
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv
import json

def pretty_print_event(event):
    """Pretty prints an event with truncation for long content."""
    if "content" not in event:
        print(f"[{event.get('author', 'unknown')}]: {event}")
        return
        
    author = event.get("author", "unknown")
    parts = event["content"].get("parts", [])
    
    for part in parts:
        if "text" in part:
            text = part["text"]
            # Truncate long text to 200 characters
            if len(text) > 200:
                text = text[:197] + "..."
            print(f"[{author}]: {text}")
        elif "functionCall" in part:
            func_call = part["functionCall"]
            print(f"[{author}]: Function call: {func_call.get('name', 'unknown')}")
            # Truncate args if too long
            args = json.dumps(func_call.get("args", {}))
            if len(args) > 100:
                args = args[:97] + "..."
            print(f"  Args: {args}")
        elif "functionResponse" in part:
            func_response = part["functionResponse"]
            print(f"[{author}]: Function response: {func_response.get('name', 'unknown')}")
            # Truncate response if too long
            response = json.dumps(func_response.get("response", {}))
            if len(response) > 100:
                response = response[:97] + "..."
            print(f"  Response: {response}")

load_dotenv()

vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
)

AGENT_ENGINE_ID = os.getenv("AGENT_ENGINE_ID")

agent_engine = agent_engines.get(AGENT_ENGINE_ID)

session = agent_engine.create_session(user_id="123")

queries = [
    "Hi, how are you?",
    "I need a venue for a hackathon for 40 people in San Francisco",
    "I need a venue for a wedding for 200 people in Seattle",
    "Find me a place for a 20 person retirement party.",
]

for query in queries:
    print(f"\n[user]: {query}")
    for event in agent_engine.stream_query(
        user_id="123",
        session_id=session['id'],
        message=query,
    ):
        pretty_print_event(event)
