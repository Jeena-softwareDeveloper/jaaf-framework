import os
os.environ["OPENAI_API_KEY"] = "sk-dummy"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"

from crewai import Agent, Crew, Process, Task
from langchain_ollama import ChatOllama

def test():
    llm = ChatOllama(model="gpt-oss:120b-cloud", base_url="http://localhost:11434")
    agent = Agent(role="Tester", goal="Test", backstory="Test", llm=llm, allow_delegation=False)
    task = Task(description="say hi", expected_output="hi", agent=agent)
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    res = crew.kickoff()
    print("Result:", res)

test()
