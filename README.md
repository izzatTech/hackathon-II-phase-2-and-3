# Hackathon II – Spec-Driven Evolution of Todo (AI-Native Cloud Application)

## Overview
This project implements a Todo application that evolves through five phases—from an in-memory console app to a distributed, cloud-native, AI-powered system—using strict Spec-Driven Development with Claude Code and Spec-Kit Plus.

## The Five Phases

### Phase I: Foundation (Console App)
- In-memory Python console application
- Basic task CRUD operations
- No persistence

### Phase II: Full-Stack Web System
- Full-stack web application with authentication and persistence
- REST API with FastAPI
- Database persistence with SQLModel and PostgreSQL

### Phase III: AI Agent & MCP Integration
- AI-powered conversational interface using Model Context Protocol (MCP) tools
- Natural language task management
- MCP-compliant tool exposure

### Phase IV: Local Kubernetes Deployment
- Local Kubernetes deployment with Minikube
- Dockerized services
- Helm charts for deployment

### Phase V: Cloud-Native Event-Driven System
- Cloud deployment with event-driven architecture
- Kafka for messaging
- Dapr for infrastructure abstraction

## Tech Stack

- **Backend**: Python 3.13+, FastAPI, SQLModel
- **Frontend**: Next.js (App Router)
- **Database**: Neon Serverless PostgreSQL
- **AI/ML**: OpenAI Agents SDK
- **MCP**: Model Context Protocol SDK
- **Containerization**: Docker
- **Orchestration**: Kubernetes, Helm
- **Runtime**: Dapr
- **Messaging**: Kafka

## Getting Started

### Prerequisites
- Python 3.13+
- Node.js 18+
- Docker and Docker Compose
- Kubernetes CLI (kubectl)
- Minikube

### Setup
1. Clone the repository
2. Set up environment variables (see `.env.example`)
3. Follow the quickstart guide in `specs/1-todo-evolution/quickstart.md`

## Project Structure

```
backend/          # Python backend with FastAPI
├── src/
│   ├── models/      # Data models
│   ├── services/    # Business logic
│   ├── api/         # API endpoints
│   ├── repositories/ # Data access layer
│   ├── utils/       # Utility functions
│   └── middleware/  # Middleware components
frontend/         # Next.js frontend
├── src/
│   ├── components/  # React components
│   ├── pages/       # Next.js pages
│   └── services/    # Frontend services
agent/            # AI agent and MCP server
├── src/
│   ├── tools/       # MCP tools
│   ├── ai_agents/   # AI agent implementations
│   └── mcp_server/  # MCP server
infra/            # Infrastructure as code
├── docker/        # Docker configurations
├── k8s/           # Kubernetes manifests and Helm charts
└── dapr/          # Dapr component configurations
```

## Specifications
Specifications for each phase can be found in `specs/1-todo-evolution/`.