import streamlit as st
import requests

# Backend configuration
BACKEND_URL = "http://localhost:8000/chat"

st.title("🗓️ Google Calendar Assistant")
st.caption("I can help you manage your calendar events!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("How can I help with your calendar?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Call backend - FIXED: Send proper JSON format
    try:
        response = requests.post(
            BACKEND_URL, 
            json={"input": prompt},  # Changed to match backend Input model
            headers={"Content-Type": "application/json"}
        ).json()
        
        assistant_response = response["response"]
        tool_called = response["tool_called"]
    except Exception as e:
        assistant_response = "Sorry, I'm having trouble connecting to the assistant."
        tool_called = "Error"
        st.error(f"Backend error: {str(e)}")
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    # Show tool used in sidebar
    st.sidebar.subheader("Last Action")
    st.sidebar.code(f"Tool used: {tool_called}")