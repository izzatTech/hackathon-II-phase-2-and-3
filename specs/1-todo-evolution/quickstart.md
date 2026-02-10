# Quickstart Guide for Todo Application Evolution

## Overview
This guide provides the essential information needed to set up and run the Todo application across all five phases of evolution.

## Prerequisites
- Python 3.13+
- Node.js 18+ (for frontend development)
- Docker and Docker Compose
- Kubernetes CLI (kubectl)
- Minikube (for local Kubernetes)
- Git

## Phase I: In-Memory Console Application

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd hackathon-todo
```

2. Navigate to the backend directory:
```bash
cd backend
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run the console application:
```bash
python src/console_app.py
```

### Usage
The console application provides basic task management commands:
- `create "Task Title"` - Create a new task
- `list` - List all tasks
- `complete <task-id>` - Mark a task as complete
- `delete <task-id>` - Delete a task
- `exit` - Exit the application

## Phase II: Full-Stack Web Application

### Backend Setup
1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (copy `.env.example` to `.env`):
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the backend server:
```bash
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup
1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

### Access the Application
- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:3000`

## Phase III: AI Agent & MCP Integration

### MCP Server Setup
1. Navigate to the agent directory:
```bash
cd agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the MCP server:
```bash
python src/mcp_server.py
```

### AI Agent Configuration
The AI agent connects to the MCP server to access task management tools. The agent can be configured to use different models and behaviors.

## Phase IV: Local Kubernetes Deployment

### Minikube Setup
1. Start Minikube:
```bash
minikube start
```

2. Enable ingress addon:
```bash
minikube addons enable ingress
```

### Deployment
1. Navigate to the infra directory:
```bash
cd infra/k8s
```

2. Apply the Kubernetes manifests:
```bash
kubectl apply -f manifests/
```

3. Deploy using Helm charts:
```bash
helm install todo-app ./helm/
```

4. Access the application:
```bash
minikube service todo-frontend --url
```

### Dapr Setup
If using Dapr, initialize it in your Kubernetes cluster:
```bash
dapr init -k
```

## Phase V: Cloud-Native Event-Driven System

### Kafka Setup
1. Ensure Kafka is running in your cluster:
```bash
kubectl apply -f infra/k8s/kafka/
```

### Event Processing
Event-driven features such as reminders and recurring tasks are handled through Kafka topics. The system publishes events to appropriate topics which are consumed by various services.

### Monitoring
Access monitoring dashboards:
```bash
kubectl port-forward svc/grafana 3000:80
```

## Development Commands

### Running Tests
- Backend: `pytest`
- Frontend: `npm run test`
- Integration: `pytest tests/integration/`

### Building Containers
```bash
docker-compose build
```

### Environment Variables
Required environment variables for each phase:
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT signing key
- `OPENAI_API_KEY` - OpenAI API key (for Phase III+)
- `MCP_SERVER_URL` - MCP server endpoint (for Phase III+)

## Troubleshooting

### Common Issues
1. **Port conflicts**: Check if required ports (8000, 3000, 8080) are available
2. **Database connection**: Verify `DATABASE_URL` in environment variables
3. **Authentication**: Ensure JWT tokens are properly configured
4. **Kubernetes**: Confirm cluster is running and `kubectl` is configured

### Phase Transition
Each phase builds upon the previous one. Ensure Phase N is working correctly before proceeding to Phase N+1.