from crewai import Task

class BaseTask:
    def __init__(self, description, agent, expected_output):
        self.task = Task(
            description=description,
            agent=agent,
            expected_output=expected_output
        )

    def execute(self):
        """Execute the task and return the result."""
        return self.task.execute() 