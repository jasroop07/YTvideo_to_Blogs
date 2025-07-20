import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
from youtube_transcript_api import YouTubeTranscriptApi
from pydantic import BaseModel, Field
from typing import Type
from langchain_groq import ChatGroq

# --- Load Environment Variables ---
load_dotenv()
print("✅ Environment variables loaded.")

# --- 1. Define the Tool ---

# This function remains the same
def extract_transcript_details(youtube_video_url: str):
    try:
        video_id = youtube_video_url.split("v=")[-1].split("&")[0]
        if 'youtu.be' in youtube_video_url:
            video_id = youtube_video_url.split('/')[-1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([i["text"] for i in transcript_text])
    except Exception as e:
        return f"Failed to get transcript for {youtube_video_url}. Error: {e}"

# Pydantic schema for robust input validation
class TranscriptInput(BaseModel):
    """Input schema for the YouTube Transcript Extractor tool."""
    youtube_video_url: str = Field(..., description="The URL of the YouTube video.")

# The custom tool definition
class TranscriptTool(BaseTool):
    name: str = "YouTube Transcript Extractor"
    description: str = "Extracts the full text transcript from a given YouTube video URL."
    args_schema: Type[BaseModel] = TranscriptInput

    def _run(self, youtube_video_url: str) -> str:
        return extract_transcript_details(youtube_video_url)

print("✅ TranscriptTool defined.")

# --- 2. Define the Agent ---

# Initialize the LLM
from crewai import LLM

llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key = os.getenv("GEMINI_API_KEY"),  # Your actual key
    temperature=0.7,
)
print("✅ LLM initialized.")

# Create the single agent
transcript_agent = Agent(
    role="YouTube Transcript Specialist",
    goal='To get the transcript of a given YouTube video',
    verbose=True,
    memory=True,
    backstory=(
        "An expert in extracting textual content from multimedia sources, "
        "you are crucial for the initial data gathering phase."
    ),
    tools=[TranscriptTool()], # Give the tool to the agent
    llm=llm,
    allow_delegation=False # No delegation needed for this simple test
)
print("✅ Agent created.")

# --- 3. Define the Task ---

research_task = Task(
    description=(
        "Extract the full transcript from the YouTube video at this URL: {youtube_video_url}. "
        "Use the YouTube Transcript Extractor tool."
    ),
    expected_output="The complete text transcript of the YouTube video as a single string.",
    agent=transcript_agent
)
print("✅ Task created.")

# --- 4. Create and Run the Crew ---

# Create the crew with the single agent and task
crew = Crew(
    agents=[transcript_agent],
    tasks=[research_task],
    process=Process.sequential
)
print("✅ Crew created. Kicking off now...")
print("-" * 50)

# Kick off the crew's work
result = crew.kickoff(inputs={'youtube_video_url': 'https://www.youtube.com/watch?v=84pxFTPsVkY'})

print("-" * 50)
print("✅ Crew finished.")
print("\nFINAL RESULT:\n")
print(result)
