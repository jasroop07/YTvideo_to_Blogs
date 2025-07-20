import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import LLM

# 1. Initialize the LLM
# Make sure to have the GOOGLE_API_KEY environment variable set
# llm = ChatGoogleGenerativeAI(
#     model="gemini-pro",
#     verbose=True,
#     temperature=0.5,
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )
from crewai import LLM

llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key = os.getenv("GEMINI_API_KEY"),  # Your actual key
    temperature=0.7,
)

# 2. Initialize the Tool
# Make sure to have the SERPER_API_KEY environment variable set
# This tool allows the agent to perform web searches.
search_tool = SerperDevTool()

# 3. Define the Research Agent
# This agent is responsible for searching for information and analyzing it.
researcher = Agent(
  role='Senior Research Analyst',
  goal='Uncover cutting-edge developments in AI and data science in 2025',
  backstory="""You are a renowned Senior Research Analyst at a leading tech think tank.
  Your expertise lies in identifying emerging trends and analyzing their potential impact.
  You are known for your insightful, data-driven reports.""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool],
  llm=llm
)

# 4. Define the Research Task
# This task instructs the agent on what to research and what the expected outcome is.
research_task = Task(
  description="""Conduct a comprehensive analysis of the latest advancements in AI in 2025.
  Identify key trends, breakthrough technologies, and potential industry impacts.
  Compile your findings into a detailed report.""",
  expected_output="A comprehensive, 3-paragraph research report in markdown format, summarizing the key AI advancements of 2025.",
  agent=researcher
)

# 5. Form the Crew
# This creates the crew, assigning the agent and the task.
# The process is sequential, meaning tasks will be executed one after another.
crew = Crew(
  agents=[researcher],
  tasks=[research_task],
  process=Process.sequential # Set to 2 for detailed logging of the execution process
)




# 6. Kickoff the Crew's Work
# This starts the execution of the tasks by the crew.
print("######################")
print("## Kicking off the Crew! 🚀")
print("######################")

result = crew.kickoff()

# 7. Print the Final Result
print("\n\n######################")
print("## Crew Execution Finished! ✅")
print("######################\n")
print("Final Result:")
print(result)