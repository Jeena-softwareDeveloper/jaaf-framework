from core.agents import support_agent
from crewai import Task, Crew
import os

def test_crew():
    print("Testing CrewAI with support_agent...")
    task = Task(
        description="Say hello to the customer.",
        agent=support_agent,
        expected_output="A greeting."
    )
    crew = Crew(agents=[support_agent], tasks=[task], verbose=True)
    try:
        result = crew.kickoff()
        print(f"Crew Result: {result}")
    except Exception as e:
        print(f"Crew Failed: {e}")

if __name__ == "__main__":
    test_crew()
