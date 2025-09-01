# 🤖 Educational Chatbot Application

An AI-powered educational chatbot application built with modern microservices architecture, designed to help students with their studies through intelligent document processing and conversational AI.

**Latest Update**: Restructured to platform-ready microservices architecture - September 1, 2025

## 🌟 Features

### Frontend Dashboard
- **Modern React Interface**: Responsive web application with intuitive chat interface
- **Real-time Conversations**: Live chat with AI-powered educational assistant
- **Document Upload**: Support for PDF, TXT, and DOCX file uploads
- **Interactive Learning**: Context-aware responses based on uploaded documents
- **User Management**: Session management and conversation history

### Backend AI Services
- **FastAPI Framework**: High-performance Python backend with automatic API documentation
- **Document Processing**: Advanced text extraction and chunking capabilities
- **Vector Search**: FAISS-powered semantic search for document similarity
- **AI Integration**: OpenAI API integration for intelligent responses
- **Health Monitoring**: Comprehensive health checks and metrics endpoints

### Platform Integration
- **Kubernetes Native**: Optimized for Kubernetes deployment with Helm charts
- **GitOps Ready**: Full CI/CD pipeline with ArgoCD integration
- **Monitoring Integration**: Prometheus metrics and Grafana dashboards
- **Security**: Network policies, RBAC, and secret management
- **Scalability**: Horizontal pod autoscaling and resource optimization

## 🏗️ Architecture

### Microservices Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Load Balancer (HTTPS)                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  Frontend (React)                          │
│             ┌─────────────────────────┐                    │
│             │   Chat Interface        │                    │
│             │   Document Upload       │                    │
│             │   User Management       │                    │
│             └─────────────────────────┘                    │
└─────────────────────┬───────────────────────────────────────┘
                      │ API Calls
┌─────────────────────▼───────────────────────────────────────┐
│               Backend (FastAPI)                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │  Chat API   │ │   AI/ML     │ │    Document             │ │
│  │  Endpoints  │ │   Service   │ │    Processing           │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────┘
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
    ┌─────────────┐    ┌─────────────────┐
    │ PostgreSQL  │    │ Persistent      │
    │ Database    │    │ Storage         │
    │             │    │ (FAISS Index)   │
    └─────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- Kubernetes cluster (for production deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/spandaai/educational-chatbot.git
   cd educational-chatbot
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Platform Deployment

The application is designed for deployment on the Spanda AI platform with automatic GitOps integration.

1. **Configure platform requirements**
   - Review and update `platform-requirements.yml`
   - Ensure your environment mappings are correct

2. **Deploy via GitOps**
   - Push to your configured branch (main/develop/staging)
   - CI/CD pipeline will automatically build and deploy
   - Monitor deployment in ArgoCD

## 📁 Project Structure

```
educational-chatbot/
├── .github/workflows/           # CI/CD pipeline configuration
├── deploy/helm/                 # Kubernetes Helm charts
│   ├── templates/              # Kubernetes manifests
│   ├── values.yaml             # Default configuration
│   ├── values-dev.yaml         # Development environment
│   ├── values-staging.yaml     # Staging environment
│   └── values-production.yaml  # Production environment
├── src/                        # Source code
│   ├── backend/                # Python FastAPI backend
│   │   ├── Dockerfile         # Backend container configuration
│   │   ├── main_api.py        # FastAPI application
│   │   ├── chunk_extractor.py # Document processing
│   │   ├── math_checker.py    # Math problem solving
│   │   └── requirements.txt   # Python dependencies
│   ├── frontend/              # React frontend
│   │   ├── Dockerfile         # Frontend container configuration
│   │   ├── nginx.conf         # Nginx configuration
│   │   ├── package.json       # Node.js dependencies
│   │   ├── public/            # Static assets
│   │   └── src/              # React source code
│   └── shared/               # Shared utilities and types
├── data/                     # Sample documents and datasets
├── platform-requirements.yml # Platform configuration
├── package.json             # Root package configuration
├── docker-compose.yml       # Local development setup
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

**Backend Configuration:**
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for AI responses
- `ENVIRONMENT`: Deployment environment (dev/staging/production)
- `LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR)

**Frontend Configuration:**
- `REACT_APP_API_URL`: Backend API endpoint
- `NODE_ENV`: Node environment (development/production)

### Platform Requirements

The `platform-requirements.yml` file configures:
- **Application Identity**: Name, repository, and team information
- **Microservices**: Auto-discovery of Docker containers
- **CI/CD Pipeline**: Build and deployment configuration
- **Infrastructure**: Required platform modules and resources
- **Environments**: Development, staging, and production settings

## 🧪 Testing

### Frontend Tests
```bash
cd src/frontend
npm test
```

### Backend Tests
```bash
cd src/backend
python -m pytest
```

### Integration Tests
```bash
docker-compose up -d
# Run integration test suite
npm run test:integration
```

## 📊 Monitoring

### Health Checks
- **Frontend**: `GET /health`
- **Backend**: `GET /health` and `GET /ready`

### Metrics
- **Prometheus**: Metrics endpoint at `/metrics`
- **Grafana**: Pre-configured dashboards for monitoring

### Logging
- **Structured Logging**: JSON format for easy parsing
- **Log Aggregation**: Centralized logging with ELK stack

## 🔒 Security

### Container Security
- **Non-root Users**: All containers run as non-root users
- **Security Contexts**: Restricted security contexts and capabilities
- **Image Scanning**: Automated vulnerability scanning with Trivy

### Network Security
- **Network Policies**: Kubernetes network policies for traffic isolation
- **TLS Encryption**: HTTPS termination and internal TLS communication
- **Secret Management**: Kubernetes secrets for sensitive data

### API Security
- **CORS Protection**: Configured CORS policies
- **Rate Limiting**: API rate limiting to prevent abuse
- **Input Validation**: Comprehensive request validation

## 🚀 Deployment

### Environments

**Development**
- Minimal resources for fast iteration
- Debug logging enabled
- Network policies disabled for easier debugging

**Staging**
- Production-like configuration
- Full monitoring enabled
- Performance testing environment

**Production**
- High availability configuration
- Horizontal pod autoscaling
- Comprehensive monitoring and alerting

### Scaling

**Horizontal Scaling**
- Frontend: 2-10 pods based on CPU/memory usage
- Backend: 2-15 pods with autoscaling policies

**Vertical Scaling**
- Configurable resource limits per environment
- Memory optimized for AI/ML workloads

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow code formatting standards (ESLint for JS, Black for Python)
- Write comprehensive tests for new features
- Update documentation for API changes
- Ensure Docker containers build successfully

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: See [docs/](docs/) for detailed documentation
- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Join community discussions in GitHub Discussions
- **Platform Support**: Contact the platform team for infrastructure issues

## 🗺️ Roadmap

- [ ] **Multi-language Support**: Internationalization and localization
- [ ] **Advanced AI Features**: Custom model fine-tuning and deployment
- [ ] **Mobile Application**: React Native mobile app
- [ ] **Voice Interface**: Speech-to-text and text-to-speech integration
- [ ] **Analytics Dashboard**: Usage analytics and insights
- [ ] **Plugin System**: Extensible plugin architecture

---

**Built with ❤️ by the Spanda AI Team**
