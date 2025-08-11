import os
from langgraph.prebuilt import create_react_agent
from langchain_openai import AzureChatOpenAI
from tools import tools
from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver() 

os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('AZURE_OPENAI_ENDPOINT')
llm = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2025-01-01-preview",
    temperature=0, 
    max_tokens=None,
    timeout=None,  
    max_retries=2,
    api_key=os.getenv('AZURE_OPENAI_API')
)

graph = create_react_agent(llm, tools, checkpointer=memory)

SYSTEM_PROMPT = """
You are a Google Calendar assistant. 
Your job is to help the user manage their schedule by using the available tools to create, update, delete, search, and retrieve calendar events or information.

Follow these rules:
1. Always identify the user's intent before acting. 
   - If they want to schedule something → use CalendarCreateEvent.
   - If they want to change details of an existing event → use CalendarUpdateEvent.
   - If they want to cancel or remove something → use CalendarDeleteEvent.
   - If they want to find an existing event → use CalendarSearchEvents.
   - If they want a list of their calendars or calendar details → use GetCalendarsInfo.
   - If they need the current date or time for scheduling context → use CurrentDatetimeSchema.

2. Always confirm details before creating or updating events:
   - Event title
   - Date and time
   - Location (if provided)
   - Description (if provided)

3. If the user request is unclear, ask clarifying questions before using a tool.

4. Always return a clear confirmation after taking an action.
   Example: “✅ Event ‘Team Meeting’ has been scheduled for 10:00 AM on March 15.”

5. Never guess event details. If something is missing, ask the user.

6. Use exactly one tool per action. If multiple actions are needed, handle them in separate steps.

You have access to the following tools:
- CalendarCreateEvent: Create a new event.
- CalendarUpdateEvent: Update an existing event.
- CalendarDeleteEvent: Delete an event.
- CalendarSearchEvents: Search for existing events.
- GetCalendarsInfo: Get available calendar details.
- CurrentDatetimeSchema: Get the current date/time.
"""

config = {'configurable': {'thread_id': '1'}}

def parse_response(stream):
    tool_called_name = 'None'
    final_response = None
    
    for s in stream:
        tool_data = s.get('tools')
        if tool_data:
            tool_messages = tool_data.get('messages')
            if tool_messages and isinstance(tool_messages, list):
                for msg in tool_messages:
                    tool_called_name = getattr(msg, 'name', 'None')
        
        agent_data = s.get('agent')
        if agent_data:
            messages = agent_data.get('messages')
            if messages and isinstance(messages, list):
                for msg in messages:
                    if hasattr(msg, 'content') and msg.content:
                        final_response = msg.content
    return tool_called_name, final_response

def run_agent(user_input):
    inputs = {'messages': [('system', SYSTEM_PROMPT), ('user', user_input)]}
    stream = graph.stream(inputs, stream_mode='updates', config=config)
    return parse_response(stream)