from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import TranscriptTool,SummarizeTool
from dotenv import load_dotenv
load_dotenv()
import os
from crewai import LLM


## call the gemini models
llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key = os.getenv("GEMINI_API_KEY"),  # Your actual key
    temperature=0.7,
)

# Creating a senior researcher agent with memory and verbose mode

transcript_agent=Agent(
    role="transcript_agent",
    goal='To get transcript of this youtube video',
    verbose=True,
    memory=True,
    backstory=(
        "Driven by curiosity, you're at the forefront of"
        "innovation, eager to explore and share knowledge that could change"
        "the world."

    ),
    tools=[TranscriptTool()],
    llm=llm,
    allow_delegation=True

)


summarize_agent= Agent(
  role='summarize_agent',
  goal='summarize this transcript into a blog post ',
  verbose=True,
  memory=True,
  backstory=(
    "With a flair for simplifying complex topics, you craft"
    "engaging narratives that captivate and educate, bringing new"
    "discoveries to light in an accessible manner."
  ),
  tools=[SummarizeTool()],
  llm=llm,
  allow_delegation=False
)

blog_agent= Agent(
    role='blog_agent',
    goal='Generate a blog post based on the summarized transcript',
    verbose=True,
    memory=True,
    backstory=(
        "As a creative writer, you weave narratives that"
        "inform and inspire, transforming complex ideas into engaging"
        "stories that resonate with readers."
    ),
    tools=[],
    llm=llm,
    allow_delegation=False
)

topic_agent = Agent(
    role='blog_topic_generator',
    goal='Generate an apt, attention-grabbing topic or title based on the content of the blog post',
    verbose=True,
    memory=True,
    backstory=(
        "As a skilled headline writer and content strategist, you read full blog posts and extract their core message. "
        "You then craft titles that are clear, engaging, and accurately represent the blog's content while drawing readers in."
    ),
    tools=[],  # no tools needed unless you're analyzing something external
    llm=llm,
    allow_delegation=False
)



