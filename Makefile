# AI Module Framework Makefile

.PHONY: help up down logs clean cli streamlit

help: ## Show this help message
	@echo "AI Module Framework - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start the AI agent
	@echo "Starting AI Module Framework..."
	docker-compose up -d
	@echo "Framework started! Access at:"
	@echo "  - API: http://localhost:8000"
	@echo "  - Chat endpoint: http://localhost:8000/chat"

down: ## Stop the framework
	@echo "Stopping AI Module Framework..."
	docker-compose down

logs: ## Show logs
	docker-compose logs -f

clean: ## Clean up
	@echo "Cleaning up..."
	docker-compose down -v --remove-orphans

cli: ## Run CLI (requires agent to be running)
	@echo "Starting CLI..."
	python src/apps/cli.py

chat: ## Start terminal chat with AI (requires agent to be running)
	@echo "Starting terminal chat..."
	python src/apps/terminal_chat.py

streamlit: ## Run Streamlit app (requires agent to be running)
	@echo "Starting Streamlit app..."
	streamlit run src/apps/streamlit_app.py