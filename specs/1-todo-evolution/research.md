# Research for Todo Application Evolution

## Phase I: In-Memory Console Application

### Decision: Technology Stack for Console App
- **Decision**: Use Python 3.13+ with console interface
- **Rationale**: Aligns with constitution requirements and provides foundation for phase evolution
- **Alternatives considered**: Node.js, Go, Java - chose Python for consistency with backend requirements

## Phase II: Full-Stack Web System

### Decision: Frontend Framework
- **Decision**: Next.js with App Router
- **Rationale**: Required by constitution, provides excellent SSR capabilities and developer experience
- **Alternatives considered**: React + Vite, Vue, Angular - Next.js mandated by constitution

### Decision: Backend Framework
- **Decision**: FastAPI with SQLModel
- **Rationale**: Required by constitution, provides excellent type safety and automatic API documentation
- **Alternatives considered**: Django, Flask, Express - FastAPI mandated by constitution

### Decision: Authentication Method
- **Decision**: Better Auth + JWT
- **Rationale**: Aligns with functional requirements, provides secure, scalable authentication
- **Alternatives considered**: Session-based, OAuth-only - JWT provides better scalability

## Phase III: AI Agent & MCP Integration

### Decision: AI Provider
- **Decision**: OpenAI Agents SDK
- **Rationale**: Required by constitution, provides robust agent capabilities
- **Alternatives considered**: Anthropic Claude, Custom LLM integration - OpenAI mandated by constitution

### Decision: MCP Tool Boundaries
- **Decision**: Strict separation between AI agent and backend via MCP-compliant tools
- **Rationale**: Enforces proper architecture, prevents direct database access from agents
- **Alternatives considered**: Direct API calls from agent - MCP tools provide better governance

## Phase IV: Local Kubernetes Deployment

### Decision: Local Kubernetes Solution
- **Decision**: Minikube for local deployment
- **Rationale**: Required by constitution, mirrors production architecture
- **Alternatives considered**: Docker Compose, Kind, K3s - Minikube mandated by constitution

### Decision: Service Mesh
- **Decision**: Dapr for infrastructure abstraction
- **Rationale**: Required by constitution, provides state management, service discovery, and secrets
- **Alternatives considered**: Istio, Linkerd - Dapr mandated by constitution

## Phase V: Cloud-Native Event-Driven System

### Decision: Event Streaming Platform
- **Decision**: Kafka (via Dapr pub/sub abstraction)
- **Rationale**: Required by constitution, supports event-driven architecture for reminders and recurring tasks
- **Alternatives considered**: RabbitMQ, Apache Pulsar - Kafka mandated by constitution

### Decision: State Management Strategy
- **Decision**: Dapr state stores for conversation and session state
- **Rationale**: Required by constitution, maintains statelessness of services while preserving needed data
- **Alternatives considered**: Direct database access - Dapr provides better abstraction

## Architecture Patterns

### Decision: Monorepo vs Polyrepo
- **Decision**: Monorepo approach
- **Rationale**: Required by constitution, simplifies dependency management and enables phased evolution
- **Alternatives considered**: Separate repositories for each component - monorepo mandated by constitution

### Decision: Database Strategy
- **Decision**: Neon Serverless PostgreSQL
- **Rationale**: Required by constitution, provides serverless scalability and PostgreSQL compatibility
- **Alternatives considered**: SQLite, MongoDB, other PostgreSQL providers - Neon mandated by constitution

### Decision: Containerization Strategy
- **Decision**: Separate containers for frontend, backend, and agent services
- **Rationale**: Enables independent scaling and deployment in Kubernetes
- **Alternatives considered**: Single container with all services - separate containers provide better scalability

### Decision: Configuration Management
- **Decision**: Environment variables with Dapr secrets for sensitive data
- **Rationale**: Maintains security while enabling configuration across environments
- **Alternatives considered**: Configuration files, in-app settings - env vars + Dapr secrets is more secure

### Decision: API Contract Approach
- **Decision**: REST APIs with OpenAPI specification for backend services
- **Rationale**: Provides clear contracts between components, supports frontend integration
- **Alternatives considered**: GraphQL, gRPC - REST provides simplicity for the use case