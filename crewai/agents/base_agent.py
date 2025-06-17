from crewai import Agent
from langchain.tools import tool

class BaseAgent:
    def __init__(self, name, role, goal, backstory):
        self.agent = Agent(
            name=name,
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=True,
            allow_delegation=False
        )

    @tool
    def analyze_data(self, data):
        """Analyze the provided data and return insights."""
        return f"Analysis of data: {data}"

    @tool
    def generate_report(self, analysis):
        """Generate a report based on the analysis."""
        return f"Report based on analysis: {analysis}" 