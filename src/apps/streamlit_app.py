"""
Simple Streamlit app for the AI Module Framework
"""

import streamlit as st
import requests
import json

# Configuration
API_URL = "http://localhost:8000"

def main():
    st.set_page_config(
        page_title="AI Module Framework",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 AI Module Framework")
    st.markdown("Simple AI agent with ontology support")
    
    # Sidebar for ontology management
    with st.sidebar:
        st.header("📚 Ontology Management")
        
        # List ontologies
        if st.button("🔄 Refresh Ontologies"):
            try:
                response = requests.get(f"{API_URL}/ontologies")
                data = response.json()
                st.session_state.ontologies = data.get('ontologies', [])
            except Exception as e:
                st.error(f"Error loading ontologies: {e}")
        
        # Load ontology
        if 'ontologies' in st.session_state and st.session_state.ontologies:
            selected_ontology = st.selectbox(
                "Select ontology to load:",
                st.session_state.ontologies
            )
            
            if st.button("📥 Load Ontology"):
                try:
                    response = requests.post(
                        f"{API_URL}/load-ontology-from-storage",
                        json={"message": selected_ontology}
                    )
                    data = response.json()
                    if 'message' in data:
                        st.success(data['message'])
                    else:
                        st.error(data.get('error', 'Unknown error'))
                except Exception as e:
                    st.error(f"Error loading ontology: {e}")
        
        # Show current context
        if st.button("👁️ Show Context"):
            try:
                response = requests.get(f"{API_URL}/ontology-context")
                data = response.json()
                context = data.get('context', 'No context loaded')
                st.text_area("Current Ontology Context:", context, height=200)
            except Exception as e:
                st.error(f"Error loading context: {e}")
    
    # Main chat interface
    st.header("💬 Chat with AI")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about the ontology..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={"message": prompt}
                    )
                    data = response.json()
                    ai_response = data.get('response', 'No response received')
                    
                    st.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    
                except Exception as e:
                    error_msg = f"Error: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()