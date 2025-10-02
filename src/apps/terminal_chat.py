#!/usr/bin/env python3
"""
Terminal Chat Interface for AI Agent
"""

import requests
import json

class TerminalChat:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
        self.load_default_ontology()
    
    def load_default_ontology(self):
        """Load the example ontology by default"""
        try:
            response = requests.post(
                f"{self.api_url}/load-ontology-from-storage",
                json={"message": "example_ontology.json"},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if 'message' in data:
                    print("✅ Loaded example ontology")
                else:
                    print("⚠️  Could not load ontology")
            else:
                print("⚠️  Could not load ontology")
        except Exception as e:
            print(f"⚠️  Could not load default ontology: {e}")
    
    def chat_with_ai(self, message):
        """Send message to AI and get response"""
        try:
            response = requests.post(
                f"{self.api_url}/chat",
                json={"message": message},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', 'No response received')
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.ConnectionError:
            return "❌ Cannot connect to AI agent. Make sure it's running with 'make up'"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def run(self):
        """Main chat loop"""
        print("🤖 AI Agent Terminal Chat")
        print("=" * 50)
        print("Type 'quit', 'exit', or 'bye' to end the conversation")
        print("Type 'help' for available commands")
        print("=" * 50)
        
        while True:
            try:
                # Get user input
                user_input = input("\n👤 You: ").strip()
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if user_input.lower() == 'context':
                    self.show_context()
                    continue
                
                if user_input.lower() == 'status':
                    self.show_status()
                    continue
                
                if not user_input:
                    continue
                
                # Send to AI and get response
                print("🤖 AI: ", end="", flush=True)
                response = self.chat_with_ai(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break
    
    def show_help(self):
        """Show help information"""
        print("\n📚 Available Commands:")
        print("  help     - Show this help message")
        print("  context  - Show current ontology context")
        print("  status   - Check AI agent status")
        print("  quit     - Exit the chat")
        print("\n💡 Just type your question to chat with the AI!")
    
    def show_context(self):
        """Show current ontology context"""
        try:
            response = requests.get(f"{self.api_url}/ontology-context", timeout=5)
            if response.status_code == 200:
                data = response.json()
                context = data.get('context', 'No context available')
                print(f"\n📖 Current Ontology Context:")
                print("-" * 40)
                print(context)
            else:
                print("❌ Could not retrieve context")
        except Exception as e:
            print(f"❌ Error getting context: {e}")
    
    def show_status(self):
        """Check AI agent status"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"\n✅ AI Agent Status: Running")
                print(f"🔗 API URL: {self.api_url}")
                print(f"🤖 Model URL: {data.get('model_url', 'Unknown')}")
            else:
                print(f"\n❌ AI Agent Status: Error ({response.status_code})")
        except Exception as e:
            print(f"\n❌ AI Agent Status: Cannot connect - {e}")

if __name__ == "__main__":
    chat = TerminalChat()
    chat.run()
