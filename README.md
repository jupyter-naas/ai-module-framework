# AI Module Framework

An intelligent AI agent framework that uses ontologies as the foundation for knowledge-driven conversations. Built with the ABI (AI Business Intelligence) architecture, this framework provides ontology-bound AI agents that strictly adhere to structured knowledge bases.

## 🚀 Quick Start

1. **Clone and start:**
   ```bash
   git clone <your-repo>
   cd ai-module-framework
   make up
   ```

2. **Chat with the AI agent:**
   ```bash
   make chat
   ```

That's it! The agent automatically loads the example ontology and you can start having intelligent conversations about the knowledge base.

## 🎯 Key Features

- **Ontology-Bound Intelligence**: AI agent strictly adheres to loaded ontology context
- **Terminal Chat Interface**: Direct command-line interaction with the AI
- **ABI Architecture**: Full framework structure with agents, ontologies, workflows, integrations, and pipelines
- **Docker-First**: Containerized deployment with Ollama integration
- **Knowledge Management**: Load, store, and query ontologies from persistent storage

## 🏗️ Architecture

```
src/
├── agents/          # AI agent implementations
├── ontologies/      # Ontology loading and management
├── workflows/       # Workflow orchestration
├── integrations/    # External system integrations
├── pipelines/       # Data processing pipelines
└── apps/           # Applications (CLI, API, Streamlit)
```

## 🛠️ Commands

```bash
make up          # Start the AI agent
make down        # Stop the framework
make chat        # Terminal chat interface
make cli         # CLI interface
make streamlit   # Web interface
make logs        # View logs
make clean       # Clean up
```

## 📡 API Endpoints

- `GET /` - Framework status and endpoints
- `GET /ontologies` - List available ontologies
- `POST /load-ontology` - Upload new ontology file
- `POST /load-ontology-from-storage` - Load ontology from storage
- `POST /chat` - Chat with AI using ontology context
- `GET /ontology-context` - View current ontology context
- `POST /query-ontology` - Direct ontology queries

## 🧠 AI Agent Behavior

The AI agent is designed with **strict ontology boundaries**:

- ✅ **Answers questions** about entities, relationships, and processes in the loaded ontology
- ❌ **Rejects off-topic questions** with clear boundary enforcement
- 🎯 **Uses direct, conversational language** (no academic jargon)
- 🔒 **Never deviates** from the provided ontology context

## 📁 Storage

- `storage/` - Persistent ontology storage
- `storage/example_ontology.json` - Sample company knowledge base

## 🔧 Requirements

- Docker
- Ollama with `qwen2.5-coder:7b` model
- Python 3.11+

## 🎯 Use Cases

- **Knowledge Base Q&A**: Ask questions about organizational structures, processes, and entities
- **Ontology Analysis**: Understand relationships and patterns in structured data
- **Domain-Specific AI**: Create specialized AI assistants for specific knowledge domains
- **Business Intelligence**: Query and analyze business ontologies and workflows