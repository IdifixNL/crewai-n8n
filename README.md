# CrewAI + n8n Hybrid Automation System

A powerful automation platform that combines CrewAI's intelligent agent framework with n8n's visual workflow orchestration, backed by local AI models via Ollama.

## 🎯 **System Overview**

This system creates an intelligent automation pipeline where:
- **n8n** provides visual workflow design and orchestration
- **CrewAI** delivers specialized AI agents with defined roles and capabilities  
- **OpenAI** provides state-of-the-art models (GPT-4, recommended for best performance)
- **Ollama** serves local AI models (CodeLlama 70B, Mixtral) as a privacy-focused alternative
- **Open-WebUI** offers direct chat interface with AI models

### **Key Use Cases**
- 📈 **Automated Trading Strategy Generation** (long-only positions)
- 🏗️ **Terraform Module Creation & Optimization**
- 🔄 **Auto-looping Workflows** until target conditions are met (e.g., 20% ROI)
- 🤖 **Multi-agent Collaboration** with specialized roles

## 🏗️ **Architecture**

```
┌─────────────┐    HTTP/REST    ┌─────────────┐    Python    ┌─────────────┐
│     n8n     │ ────────────── │   CrewAI    │ ───────────── │   Ollama    │
│  Workflows  │                │   Agents    │               │   Models    │
└─────────────┘                └─────────────┘               └─────────────┘
       │                              │                             │
       │        ┌─────────────┐       │                             │
       └────────│ Open-WebUI  │───────┘                             │
                │    Chat     │─────────────────────────────────────┘
                └─────────────┘
```

### **Data Flow**
1. **n8n Trigger** → Manual, scheduled, or webhook-based
2. **HTTP Request** → `POST http://crewai:8000/run-agent`
3. **CrewAI Processing** → Specialized agents analyze and execute tasks
4. **Ollama Integration** → Local AI models provide intelligence
5. **Response Handling** → Results flow back through n8n for further processing

## 🚀 **Quick Start**

### **Prerequisites**
- Docker & Docker Compose installed
- **OpenAI API Key** (recommended for best performance)
- 16GB+ RAM (only needed if using local Ollama models)
- Git for version control

### **1. Clone & Setup**
```bash
git clone git@github.com:IdifixNL/crewai-n8n.git
cd crewai-n8n

# Copy environment template
cp .env.example .env
# Add your OpenAI API key to .env (recommended for best performance)
# OPENAI_API_KEY=your_actual_api_key_here
```

### **2. Start the System**
```bash
# Start all services
docker compose up -d

# Check status
docker compose ps
```

### **3. Access the Interfaces**
- **n8n Workflows**: http://localhost:5678
  - Username: `admin`
  - Password: `securepassword`
- **Open-WebUI Chat**: http://localhost:3000
- **CrewAI API**: http://localhost:8000
- **API Health Check**: http://localhost:8000/health

### **4. AI Model Setup**

#### **Option A: OpenAI (Recommended)**
The system is pre-configured to use OpenAI models. Simply add your API key to `.env`:
```bash
# In your .env file
OPENAI_API_KEY=your_actual_api_key_here
```
**Benefits**: Superior performance, faster responses, no local resource requirements.

#### **Option B: Local Ollama Models (Privacy-focused)**
```bash
# Download CodeLlama 70B (primary local model)
docker exec crewai-n8n-ollama-1 ollama pull codellama:70b-instruct

# Download Mixtral (backup local model)  
docker exec crewai-n8n-ollama-1 ollama pull mixtral:instruct

# List available models
docker exec crewai-n8n-ollama-1 ollama list
```
**Benefits**: Complete privacy, no external API calls, one-time download.

## 🤖 **CrewAI API Reference**

### **Base URL**
- **External**: `http://localhost:8000`
- **From n8n (Docker)**: `http://crewai:8000`

### **Endpoints**

#### **Health Check**
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy"
}
```

#### **Run Agent Task**
```http
POST /run-agent
Content-Type: application/json

{
  "task": "Generate a trading strategy for EURUSD"
}
```

**Response:**
```json
{
  "status": "ok",
  "result": "Task received: Generate a trading strategy for EURUSD. CrewAI agent system is ready for configuration."
}
```

## 📁 **Project Structure**

```
crewai-n8n/
├── crewai/                     # CrewAI agent system
│   ├── agents/                 # Agent definitions
│   │   ├── __init__.py
│   │   └── base_agent.py       # Base agent template
│   ├── tasks/                  # Task definitions  
│   │   ├── __init__.py
│   │   └── base_task.py        # Base task template
│   ├── __init__.py
│   └── main.py                 # FastAPI application
├── n8n-flows/                  # n8n workflow exports (private - not in git)
├── workspace/                  # Safe output directory
├── docs/                       # Documentation
├── docker-compose.yml          # Service orchestration
├── Dockerfile                  # CrewAI container build
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .gitignore                  # Git exclusions
└── README.md                   # This file
```

## 🔧 **n8n Workflow Setup**

### **Basic CrewAI Integration**

1. **Create New Workflow** in n8n
2. **Add Manual Trigger** or schedule trigger
3. **Add HTTP Request Node:**
   - Method: `POST`
   - URL: `http://crewai:8000/run-agent`
   - Body Type: `JSON`
   - Body Parameters:
     ```json
     {
       "task": "{{ $json.task || 'Default task description' }}"
     }
     ```

### **Advanced Workflow Patterns**

#### **Auto-Loop Until Target Met**
```
Trigger → HTTP Request → Code Node → Condition → Loop Back
                                   → Success → Email/Webhook
```

#### **Multi-Agent Collaboration**
```
Trigger → Strategy Agent → Risk Agent → Optimizer → Results
```

## 🛠️ **Development Workflow**

### **Creating New Agents**

1. **Create Agent File** in `crewai/agents/`:
```python
from crewai import Agent
from langchain_openai import ChatOpenAI  # Recommended
# from langchain_ollama import OllamaLLM  # Alternative for local models

class TradingStrategyAgent:
    def __init__(self):
        # Option A: OpenAI (Recommended)
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1
        )
        
        # Option B: Local Ollama (Privacy-focused)
        # self.llm = OllamaLLM(
        #     model="codellama:70b-instruct",
        #     base_url="http://ollama:11434"
        # )
        
        self.agent = Agent(
            role="Trading Strategy Analyst",
            goal="Generate profitable long-only trading strategies",
            backstory="Expert in forex analysis and strategy development",
            llm=self.llm,
            verbose=True
        )
    
    def generate_strategy(self, pair, timeframe):
        # Implementation here
        pass
```

2. **Create Task File** in `crewai/tasks/`:
```python
from crewai import Task

class StrategyGenerationTask:
    def __init__(self, agent):
        self.task = Task(
            description="Generate a trading strategy for {pair} on {timeframe}",
            agent=agent,
            expected_output="Detailed strategy with entry/exit rules"
        )
```

3. **Update Main API** in `crewai/main.py`:
```python
from agents.trading_strategy_agent import TradingStrategyAgent

@app.post("/run-agent")
async def run_agent(request: Request):
    data = await request.json()
    task_type = data.get("type", "general")
    
    if task_type == "trading_strategy":
        agent = TradingStrategyAgent()
        result = agent.generate_strategy(
            data.get("pair", "EURUSD"),
            data.get("timeframe", "1H")
        )
    
    return {"status": "ok", "result": result}
```

### **Testing Changes**

```bash
# Rebuild and restart CrewAI service
docker compose build crewai && docker compose up -d crewai

# Check logs
docker compose logs crewai -f

# Test API endpoint
curl -X POST http://localhost:8000/run-agent \
  -H "Content-Type: application/json" \
  -d '{"task": "Test task", "type": "trading_strategy"}'
```

## 📊 **Monitoring & Logs**

### **Service Status**
```bash
# Check all services
docker compose ps

# View specific service logs
docker compose logs n8n -f
docker compose logs crewai -f
docker compose logs ollama -f
```

### **Resource Usage**
```bash
# Monitor resource usage
docker stats

# Check Ollama model status
docker exec crewai-n8n-ollama-1 ollama list
```

## 🔄 **Backup & Recovery**

### **Backup n8n Workflows (Private)**
1. In n8n UI: Settings → Import/Export
2. Export workflows to local backup location
3. **Note**: Workflows are kept private (not committed to public git)

### **Backup Data Volumes**
```bash
# Backup n8n data
docker run --rm -v crewai-n8n_n8n_data:/data -v $(pwd):/backup ubuntu tar czf /backup/n8n-backup.tar.gz /data

# Backup Ollama models  
docker run --rm -v crewai-n8n_ollama_models:/data -v $(pwd):/backup ubuntu tar czf /backup/ollama-backup.tar.gz /data
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### **CrewAI Container Won't Start**
```bash
# Check logs
docker compose logs crewai

# Common fixes:
docker compose build crewai --no-cache
docker compose up -d crewai
```

#### **n8n Can't Connect to CrewAI**
- ✅ Use `http://crewai:8000` (not `localhost:8000`)
- ✅ Check if CrewAI container is running: `docker compose ps`
- ✅ Verify network connectivity: `docker compose exec n8n curl http://crewai:8000/health`

#### **Ollama Models Not Loading**
```bash
# Check available models
docker exec crewai-n8n-ollama-1 ollama list

# Pull model manually
docker exec crewai-n8n-ollama-1 ollama pull codellama:70b-instruct

# Check resource usage (models need significant RAM)
docker stats
```

### **Port Conflicts**
If ports are already in use, modify `docker-compose.yml`:
```yaml
services:
  n8n:
    ports:
      - "5679:5678"  # Change from 5678 to 5679
```

## 🛡️ **Security Considerations**

- 🔒 **Environment Variables**: Use `.env` file for secrets (never commit to git)
- 🌐 **Network Access**: Services communicate via Docker internal network
- 🔑 **n8n Authentication**: Change default credentials in production
- 🚫 **No Short Positions**: System designed for long-only trading strategies
- 🤖 **AI Models**: OpenAI (recommended) or local Ollama models for privacy
- 🔐 **API Keys**: OpenAI keys are encrypted in transit and stored securely

## 🎯 **Roadmap**

### **Phase 1: Core Intelligence (Current)**
- [x] Basic n8n ↔ CrewAI integration
- [x] Docker orchestration
- [x] Ollama model integration
- [ ] Trading strategy agents
- [ ] Risk management agents

### **Phase 2: Advanced Workflows**
- [ ] Multi-agent collaboration
- [ ] Auto-looping until target ROI
- [ ] Performance optimization agents
- [ ] Terraform module generation

### **Phase 3: Production Features**
- [ ] Advanced monitoring
- [ ] Performance analytics
- [ ] Strategy backtesting
- [ ] Alert systems

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- [CrewAI](https://github.com/joaomdmoura/crewAI) - Multi-agent framework
- [n8n](https://n8n.io/) - Workflow automation platform  
- [Ollama](https://ollama.ai/) - Local AI model serving
- [Open-WebUI](https://github.com/open-webui/open-webui) - AI chat interface
