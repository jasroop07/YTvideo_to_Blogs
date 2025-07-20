from crewai import Task
from agents import transcript_agent, summarize_agent, blog_agent, topic_agent
from tools import TranscriptTool, SummarizeTool

# It's good practice to instantiate tools once and reuse them
transcript_tool = TranscriptTool()
summarize_tool = SummarizeTool()

# --- Task Definitions ---

# Task 1: Get the transcript
# This task is the entry point and receives the initial input for the Crew.
research_task = Task(
  description=(
    "Extract the full transcript from the YouTube video at this URL: {youtube_video_url}. "
    "Use the YouTube Transcript Extractor tool."
  ),
  expected_output="The complete text transcript of the YouTube video.",
  agent=transcript_agent,
  tools=[transcript_tool]
  # No 'inputs' here because it will be provided when the Crew kicks off.
)

# Task 2: Summarize the transcript
# This task uses the output of 'research_task' as its context.
summarize_task = Task(
  description=(
    "Take the video transcript and create a detailed, concise summary. "
    "Identify the key points, main arguments, and important examples from the text."
  ),
  expected_output="A well-structured summary of the video transcript, capturing all essential information.",
  agent=summarize_agent,
  tools=[summarize_tool],
  context=[research_task] # Correct way to pass data from the previous task
)

# Task 3: Write the blog post from the summary
# This task uses the output of 'summarize_task' as its context.
write_task = Task(
  description=(
    "Using the summary of the video transcript, write a compelling and engaging blog post. "
    "The blog post should be well-structured with a clear introduction, body, and conclusion. "
    "It should have a conversational and informative tone."
  ),
  expected_output="A fully written blog post of at least 3-4 paragraphs, based on the provided summary.",
  agent=blog_agent,
  context=[summarize_task] # Correctly uses the summary from the previous task
)

# Task 4: Generate a title and format the final output
# This task takes the blog post from 'write_task' and puts the finishing touches on it.
final_output_task = Task(
  description=(
    "Read the generated blog post. Create a catchy, SEO-friendly title for it. "
    "Then, format the entire output as a single markdown file. "
    "The file should start with the title (e.g., '# My Awesome Title'), followed by the full text of the blog post."
  ),
  expected_output="A complete markdown string containing the title and the blog post.",
  agent=topic_agent,
  context=[write_task], # Correctly uses the blog post from the previous task
  output_file='new-blog-post.md' # This saves the final output to a file
)
