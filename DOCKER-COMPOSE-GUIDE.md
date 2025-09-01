# Docker Compose Usage Guide

This guide shows how to use the unified docker-compose.yml file for different scenarios.

## Quick Start

1. **Setup Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration (especially OPENAI_API_KEY)
   ```

2. **Start Development Environment**:
   ```bash
   docker-compose up
   ```

## Usage Scenarios

### 🚀 Development Mode (Default)
Start all services with hot reloading and development features:
```bash
docker-compose up
```

Services available:
- Frontend: http://localhost:3000 (with hot reload)
- Backend API: http://localhost:8000 (with auto-reload)
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 🛠️ Development with Tools
Include database and redis management tools:
```bash
docker-compose --profile tools up
```

Additional services:
- Adminer (Database UI): http://localhost:8080
- Redis Commander: http://localhost:8081

### 🎯 Production-like Testing
Test with production-like configuration:
```bash
BUILD_TARGET=production FRONTEND_COMMAND="nginx -g 'daemon off;'" BACKEND_COMMAND="uvicorn main_api:app --host 0.0.0.0 --port 8000" docker-compose --profile production up
```

### 📊 Background Services Only
Start only database and cache services:
```bash
docker-compose up postgres redis
```

## Environment Variables

Key variables you can customize in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `FRONTEND_PORT` | 3000 | Frontend port |
| `BACKEND_PORT` | 8000 | Backend API port |
| `POSTGRES_PORT` | 5432 | Database port |
| `REDIS_PORT` | 6379 | Redis port |
| `BUILD_TARGET` | builder | Docker build target (builder/production) |
| `OPENAI_API_KEY` | - | Your OpenAI API key |
| `LOG_LEVEL` | DEBUG | Backend logging level |

## Commands Reference

### Basic Operations
```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart backend

# View logs
docker-compose logs -f backend
```

### Development Operations
```bash
# Rebuild and start
docker-compose up --build

# Run with development tools
docker-compose --profile tools up

# Execute command in running container
docker-compose exec backend python manage.py migrate
```

### Data Management
```bash
# Reset database (WARNING: destroys data)
docker-compose down -v
docker volume rm chatbot-postgres-data

# Backup database
docker-compose exec postgres pg_dump -U chatbot_user educational_chatbot > backup.sql

# Import data
docker-compose exec -T postgres psql -U chatbot_user educational_chatbot < backup.sql
```

### Debugging
```bash
# Check service health
docker-compose ps

# Access service shell
docker-compose exec backend bash
docker-compose exec frontend sh

# Monitor resource usage
docker stats
```

## Profiles Explained

- **Default (no profile)**: Frontend, Backend, PostgreSQL, Redis
- **tools**: Adds Adminer and Redis Commander
- **production**: Adds Nginx reverse proxy
- **development**: Same as default but explicitly named

## Troubleshooting

### Common Issues

1. **Port conflicts**: Change ports in `.env` file
2. **Permission issues**: Run with `sudo` on Linux/Mac
3. **Build errors**: Try `docker-compose build --no-cache`
4. **Database connection**: Ensure PostgreSQL is healthy before backend starts

### Health Checks

All services have health checks. View status:
```bash
docker-compose ps
```

### Logs Investigation
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f --tail=100 backend
```

## File Structure

```
├── docker-compose.yml          # Main compose file
├── .env.example               # Environment template
├── .env                       # Your environment (create from example)
├── scripts/
│   └── init-db.sql           # Database initialization
└── src/
    ├── frontend/             # React application
    └── backend/              # FastAPI application
```
