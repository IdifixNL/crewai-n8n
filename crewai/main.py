from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# from crewai.agents.base_agent import BaseAgent

app = FastAPI()

# (Optional CORS support if you're calling from a browser/frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "CrewAI API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/run-agent")
async def run_agent(request: Request):
    data = await request.json()
    task_description = data.get("task", "")

    # Create a basic response for now (agent integration will be added later)
    result = f"Task received: {task_description}. CrewAI agent system is ready for configuration."
    return {"status": "ok", "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
