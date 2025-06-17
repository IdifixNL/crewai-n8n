import os
from crewai import Agent, Task, Crew
from langchain.tools import tool
from langchain_ollama import OllamaLLM

def test_agent_creation():
    print("Testing agent creation...")
    llm = OllamaLLM(model="codellama:70b-instruct", base_url="http://ollama:11434")
    agent = Agent(
        name="Test Agent",
        role="Test Role",
        goal="Test Goal",
        backstory="Test Backstory",
        llm=llm,
        verbose=True
    )
    print("✓ Agent created successfully")
    return agent

def test_task_creation(agent):
    print("\nTesting task creation...")
    task = Task(
        description="Test task description",
        agent=agent,
        expected_output="Test output"
    )
    print("✓ Task created successfully")
    return task

def test_crew_creation(agent, task):
    print("\nTesting crew creation...")
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
    print("✓ Crew created successfully")
    return crew

def main():
    print("Starting basic setup test...\n")
    
    # Test agent creation
    agent = test_agent_creation()
    
    # Test task creation
    task = test_task_creation(agent)
    
    # Test crew creation
    crew = test_crew_creation(agent, task)
    
    print("\nAll basic components tested successfully!")
    print("\nYou can now run the main chain using:")
    print("docker compose up -d")

if __name__ == "__main__":
    main() 