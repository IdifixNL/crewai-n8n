from crewai import Task
import os
from datetime import datetime

class TerraformModuleTask:
    def __init__(self, agent, task_description, module_type="generic", cloud_provider="azure"):
        # Generate timestamped output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = f"/app/workspace/terraform_modules/{module_type}_{timestamp}"
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.task = Task(
            description=f"""
            Generate a complete, production-ready Terraform module based on this request: {task_description}
            
            Requirements:
            1. Create a modular, reusable Terraform configuration
            2. Follow Terraform best practices and naming conventions
            3. Include proper variable definitions with descriptions and types
            4. Add comprehensive outputs for all important resource attributes
            5. Include security best practices (encryption, access controls, etc.)
            6. Generate clear documentation with usage examples
            7. Use {cloud_provider} as the cloud provider
            8. Save all files to: {self.output_dir}
            
            Required Files to Generate:
            - main.tf: Core resource definitions
            - variables.tf: Input variables with descriptions and validation
            - outputs.tf: Output values for integration with other modules
            - versions.tf: Provider version constraints
            - README.md: Comprehensive documentation with examples
            
            Additional Considerations:
            - Use consistent naming conventions
            - Add appropriate tags/labels for resource management
            - Include data sources where appropriate
            - Follow the principle of least privilege for security
            - Make the module configurable but with sensible defaults
            """,
            expected_output=f"""
            A complete Terraform module saved to {self.output_dir} containing:
            1. main.tf - Well-structured resource definitions
            2. variables.tf - Properly typed and documented variables
            3. outputs.tf - Useful outputs for module consumers
            4. versions.tf - Terraform and provider version requirements
            5. README.md - Complete documentation with usage examples
            
            The module should be immediately usable and follow all Terraform best practices.
            """,
            agent=agent
        )
    
    def get_task(self):
        return self.task
    
    def get_output_dir(self):
        return self.output_dir 