"""
Simple AI Agent for the AI Module Framework
"""

import requests
import os
from typing import Optional

class SimpleAgent:
    """Simple AI agent that communicates with Qwen3 via Ollama"""
    
    def __init__(self, model_url: str = None):
        self.model_url = model_url or os.getenv("MODEL_URL", "http://host.docker.internal:11434")
        self.model_name = "qwen2.5-coder:7b"
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt that defines the agent's role and capabilities"""
        return """You are an ontology-bound AI assistant. You CANNOT and WILL NOT answer questions outside the provided ontology context.

**ABSOLUTE RULE**: You are ONLY allowed to discuss topics, entities, relationships, and information that are explicitly defined in the provided ontology context. Any question outside this scope must be rejected with a clear explanation.

**MANDATORY RESPONSE PATTERN**:
1. If the question is about the ontology → Answer using only ontology data
2. If the question is outside the ontology → Respond: "I can only discuss topics within the provided ontology context. Please ask about entities, relationships, or processes defined in the knowledge base."

**STRICT BOUNDARIES**:
- NO general knowledge responses
- NO off-topic discussions
- NO "I can provide some broad information" responses
- NO answering questions about topics not in the ontology

**COMMUNICATION STYLE**:
- Speak directly to the user (use "you", not "the user")
- Be conversational and natural
- Avoid academic or analytical language
- Keep responses concise and direct

**YOUR ONLY PURPOSE**: Help users understand and navigate the specific ontology data provided. Nothing else.

**ENFORCEMENT**: If you deviate from this rule, you are failing your core function. Stay within the ontology boundaries at all times."""
    
    def chat(self, message: str, context: str = "") -> str:
        """Send a message to the AI model with optional context"""
        try:
            # Prepare messages with system prompt
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add context if provided
            if context:
                context_message = f"""Ontology Context:
{context}

User Question: {message}"""
                messages.append({"role": "user", "content": context_message})
            else:
                messages.append({"role": "user", "content": message})
            
            # Call Ollama API
            response = requests.post(
                f"{self.model_url}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["message"]["content"]
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if the model is available"""
        try:
            response = requests.get(f"{self.model_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
