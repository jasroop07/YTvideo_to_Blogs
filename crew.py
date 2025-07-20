from crewai import Crew, Process
from tasks import research_task, summarize_task, write_task, final_output_task
from agents import transcript_agent, summarize_agent, blog_agent, topic_agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()   

# Assemble the crew
yt_blog_crew = Crew(
    agents=[transcript_agent, summarize_agent, blog_agent, topic_agent],
    tasks=[research_task, summarize_task, write_task, final_output_task],
    process=Process.sequential,
    # Caching is recommended for development to avoid re-running completed tasks
    # memory=True, 
    # cache=True,
    # verbose=2 # You can set it to 1 or 2 for different levels of detail
)

# Kick off the crew's work
# The key 'youtube_video_url' now correctly matches the tool's expected input



# result = yt_blog_crew.kickoff(inputs={'youtube_video_url': 'https://www.youtube.com/watch?v=sq010xzuW78'})

# print("######################")
# print("## Here is the Final Result:")
# print("######################")
# print(result)
