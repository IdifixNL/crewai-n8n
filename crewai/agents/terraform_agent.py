from crewai import Agent
from langchain_openai import ChatOpenAI
from crewai_tools import FileWriterTool, DirectoryReadTool
import os

class TerraformAgent:
    def __init__(self):
        # Use OpenAI GPT-4 for best performance
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,  # Low temperature for consistent code generation
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Tools the agent can use
        self.file_writer = FileWriterTool()
        self.directory_reader = DirectoryReadTool()
        
        # Define the agent
        self.agent = Agent(
            role="Senior DevOps Engineer & Terraform Expert",
            goal="Create production-ready, secure, and well-documented Terraform modules following industry best practices",
            backstory="""You are a highly experienced DevOps engineer with 10+ years of experience in cloud infrastructure 
            and Infrastructure as Code. You specialize in Terraform and have deep knowledge of AWS, Azure, and GCP. 
            You always follow security best practices, use proper naming conventions, and create comprehensive documentation.
            You understand the importance of modularity, reusability, and maintainability in infrastructure code.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.file_writer, self.directory_reader],
            llm=self.llm
        )
    
    def get_agent(self):
        return self.agent 