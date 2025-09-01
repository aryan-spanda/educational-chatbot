# Educational Chatbot - Development Commands
# Use these commands to manage your development environment

.PHONY: help setup start stop restart logs build clean test

# Default target
help:
	@echo "Educational Chatbot Development Commands"
	@echo "========================================"
	@echo ""
	@echo "Setup & Environment:"
	@echo "  setup          - Setup environment file and start services"
	@echo "  env            - Create .env from template"
	@echo ""
	@echo "Development:"
	@echo "  start          - Start all services"
	@echo "  start-tools    - Start services with development tools"
	@echo "  stop           - Stop all services"
	@echo "  restart        - Restart all services"
	@echo "  build          - Rebuild and start services"
	@echo ""
	@echo "Monitoring:"
	@echo "  logs           - Show logs from all services"
	@echo "  logs-backend   - Show backend logs"
	@echo "  logs-frontend  - Show frontend logs"
	@echo "  status         - Show service status"
	@echo ""
	@echo "Data Management:"
	@echo "  clean          - Stop services and remove volumes"
	@echo "  reset          - Reset all data (WARNING: destroys data)"
	@echo "  backup-db      - Backup database"
	@echo ""
	@echo "Testing:"
	@echo "  test           - Run tests"
	@echo "  test-backend   - Run backend tests"
	@echo "  test-frontend  - Run frontend tests"

# Setup commands
setup: env start

env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file. Please edit it with your configuration."; \
	else \
		echo ".env file already exists."; \
	fi

# Development commands
start:
	docker-compose up -d

start-tools:
	docker-compose --profile tools up -d

stop:
	docker-compose down

restart:
	docker-compose restart

build:
	docker-compose up --build -d

# Monitoring commands
logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

status:
	docker-compose ps

# Data management
clean:
	docker-compose down
	docker system prune -f

reset:
	@echo "WARNING: This will destroy all data!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	docker-compose down -v
	docker volume rm chatbot-postgres-data chatbot-redis-data chatbot-faiss-storage 2>/dev/null || true

backup-db:
	@mkdir -p backups
	docker-compose exec postgres pg_dump -U chatbot_user educational_chatbot > backups/db-backup-$(shell date +%Y%m%d-%H%M%S).sql
	@echo "Database backed up to backups/ directory"

# Testing commands
test:
	@echo "Running all tests..."
	$(MAKE) test-backend
	$(MAKE) test-frontend

test-backend:
	docker-compose exec backend python -m pytest tests/ -v

test-frontend:
	docker-compose exec frontend npm test -- --coverage --watchAll=false

# Development helpers
shell-backend:
	docker-compose exec backend bash

shell-frontend:
	docker-compose exec frontend sh

shell-db:
	docker-compose exec postgres psql -U chatbot_user educational_chatbot
