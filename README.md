# CrewAI + n8n Hybrid Automation System

## Overview
This system uses CrewAI agents and n8n to automate workflows like:
- Generating and improving FreqAI strategies
- Building and refining Terraform modules
- Auto-looping until target conditions (e.g., 20% ROI) are met

## Key Components
- **CrewAI**: Python-based AI agents with roles and tools
- **n8n**: Visual automation platform for orchestration
- **Langchain Tools**: Enable web access for agents
- **Models**: CodeLlama 70B (main), Mixtral (backup)

## Instructions

### 1. Install Dependencies
Ensure you have Docker and Docker Compose installed.

### 2. Start the System
```bash
docker compose up -d
```

- n8n UI: http://localhost:5678
- Open-WebUI (Ollama Chat): http://localhost:3000

### 3. Add Models to Ollama
```bash
ollama pull codellama:70b-instruct
ollama pull mixtral:instruct
```

### 4. Add Your Agents
Define agents in `crewai/agents/` and tasks in `crewai/tasks/`.

### 5. Add n8n Workflows
Export .json flows and place in `n8n-flows/`.

### 6. Run a Workflow
Use n8n to trigger an agent task, analyze output, loop if needed.

## Folder Structure
- `crewai/` - Agent/task logic
- `workspace/` - Safe output location
- `n8n-flows/` - Visual workflows
- `docs/` - Diagrams and documentation
