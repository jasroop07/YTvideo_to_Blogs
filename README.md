
# YouTube to Blog Generator

This project leverages CrewAI to build an Agentic AI pipeline that converts YouTube videos into polished blog posts. It features 4 specialized agents—each handling tasks like transcription, summarization, fact-checking, and content generation—powered by custom tools and task orchestration. The system automates the end-to-end process of transforming video content into structured, readable blogs, ideal for content creators and bloggers.


## Demo

![Demo](images/yt_blog_1.gif)


## Features

🔗 YouTube Integration: Automatically fetches transcripts from YouTube videos.

🧠 Agentic Workflow: Powered by CrewAI with 4 specialized agents for each step—Transcription, Summarization, Fact-Checking, and Blog Generation.

✍️ High-Quality Blog Output: Converts video content into well-structured, readable blog posts.

📦 Modular & Extensible: Designed to easily plug in additional tools or agents based on future needs.

🤖 LLM-Powered Generation: Utilizes Gemini's GPT models for natural, human-like blog writing.



## Tech Stack

**Agent Framework:** CrewAI  
**Language Model:** Gemini (GPT-based)  
**Tools:** Custom Tools (Transcriber, Summarizer, Fact Checker, Blog Writer)  
**Backend:** Python (Flask)  
**Others:** Langchain, YouTube Transcript API, Pydantic


## Installation

Install my-project with npm

```bash
  pip install -r requirements.txt
```
    