from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from crewai import Crew, Process
from agents.terraform_agent import TerraformAgent
from tasks.terraform_task import TerraformModuleTask
import os
import json
import traceback

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
    return {"message": "CrewAI API is running with Terraform module generation"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/run-agent")
async def run_agent(request: Request):
    try:
        data = await request.json()
        task_description = data.get("task", "")
        task_type = data.get("type", "terraform_module")
        cloud_provider = data.get("cloud_provider", "azure")
        module_type = data.get("module_type", "generic")

        if not task_description:
            raise HTTPException(status_code=400, detail="Task description is required")

        # Check if OpenAI API key is available
        if not os.getenv("OPENAI_API_KEY"):
            return {
                "status": "error", 
                "result": "OpenAI API key not configured. Please add OPENAI_API_KEY to your .env file for AI-powered module generation."
            }

        if task_type == "terraform_module":
            # Create Terraform agent
            terraform_agent = TerraformAgent()
            
            # Create task for the agent
            terraform_task = TerraformModuleTask(
                agent=terraform_agent.get_agent(),
                task_description=task_description,
                module_type=module_type,
                cloud_provider=cloud_provider
            )
            
            # Create and run the crew
            crew = Crew(
                agents=[terraform_agent.get_agent()],
                tasks=[terraform_task.get_task()],
                verbose=True,
                process=Process.sequential
            )
            
            # Execute the crew
            result = crew.kickoff()
            
            return {
                "status": "success",
                "result": str(result),
                "output_directory": terraform_task.get_output_dir(),
                "message": f"Terraform module generated successfully in {terraform_task.get_output_dir()}"
            }
        else:
            # Handle other task types or fallback
            return {
                "status": "ok",
                "result": f"Task received: {task_description}. Task type '{task_type}' processed."
            }
            
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error in run_agent: {error_details}")
        return {
            "status": "error",
            "result": f"Error processing request: {str(e)}",
            "details": error_details
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
