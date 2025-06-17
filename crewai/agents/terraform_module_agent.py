from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import os

# Tool to save Terraform files
@tool
def write_terraform_module(module_name: str, main_tf: str, variables_tf: str, outputs_tf: str, readme_md: str) -> str:
    base_path = f"/app/workspace/{module_name}"
    os.makedirs(base_path, exist_ok=True)

    with open(os.path.join(base_path, "main.tf"), "w") as f:
        f.write(main_tf)
    with open(os.path.join(base_path, "variables.tf"), "w") as f:
        f.write(variables_tf)
    with open(os.path.join(base_path, "outputs.tf"), "w") as f:
        f.write(outputs_tf)
    with open(os.path.join(base_path, "README.md"), "w") as f:
        f.write(readme_md)

    return f"Terraform module written to {base_path}"

# CrewAI logic wrapper
class TerraformModuleBuilder:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.2)

        self.agent = Agent(
            role="Terraform Architect",
            goal="Generate a production-ready Terraform module based on user input",
            backstory="You are a DevOps engineer specializing in infrastructure-as-code for scalable cloud environments.",
            tools=[write_terraform_module],
            verbose=True,
            llm=self.llm
        )

    def run(self, description: str):
        task = Task(
            description=(
                f"Create a Terraform module based on this request: {description}.\n"
                "Include main.tf, variables.tf, outputs.tf, and a README.md.\n"
                "Follow Terraform best practices, use variables, outputs, and reusable structure."
            ),
            agent=self.agent
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )

        return crew.run()
