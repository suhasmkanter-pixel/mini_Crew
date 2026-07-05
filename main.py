from guard.guard import Task, Agents, ExecutionEngine

researchAgent = Agents(
    name="Research Agent",
    role="researcher",
    goal="Find accurate information",
    description="Researches a topic and provides technical details."
)

codeAgent = Agents(
    name="Code Agent",
    role="software engineer",
    goal="Write clean and working code",
    description="Generates code based on the given requirements and context."
)

reviewAgent = Agents(
    name="Code Reviewer",
    role="code reviewer",
    goal="Review and improve code quality",
    description="Finds bugs, suggests improvements, and ensures best practices."
)

task1 = Task(
    topic="Binary Search",
    description="Research Binary Search, explain how it works, its time complexity, and when it should be used.",
    agent=researchAgent
)

task2 = Task(
    topic="Python Implementation",
    description="Using the research context, write a clean Python implementation of Binary Search with comments.",
    agent=codeAgent
)

task3 = Task(
    topic="Code Review",
    description="Review the generated Python code, identify any issues, optimize it if needed, and explain the improvements.",
    agent=reviewAgent
)

execution = ExecutionEngine()

print(execution.execute_task([task1, task2, task3]))