from crewai import Agent, Task, Crew
from youtube_transcript_api import YouTubeTranscriptApi
import spacy
from nltk.tokenize import sent_tokenize
from transformers import pipeline


from crewai.tools import BaseTool
#write in terminal. python -m spacy download en_core_web_sm


#TRANSCRIPT TOOL


#TRANSCRIPT FUNCTION
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

class TranscriptTool(BaseTool):
    name: str = "YouTube Transcript Extractor"
    description: str = "Extracts transcript text from a YouTube video URL."

    def _run(self, youtube_video_url: str) -> str:
        try:
            return extract_transcript_details(youtube_video_url)
        except Exception as e:
            return f"Error extracting transcript: {str(e)}"



# transcript_tool = Tool(
#     name="transcript_tool",
#     description="Gets the transcript of a YouTube video. Input should be a valid YouTube video URL",
#     func=extract_transcript_details
# )

#SUMMARIZE TOOL


#SUMMARIZE FUNCTION


# Load required models once
import nltk
from nltk.tokenize import sent_tokenize

nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def summarize_large_text(text, max_chunk_words=600):
    """
    Preprocesses, chunks, and summarizes long text using spaCy and BART.
    
    Args:
        text (str): Raw input text (e.g. YouTube transcript).
        max_chunk_words (int): Maximum words per chunk (default 600).
    
    Returns:
        str: Final combined summary.
    """
    # Step 1: Preprocess and sentence split using spaCy
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 5]

    # Step 2: Chunk sentences based on word count
    chunks, current_chunk = [], []

    for sentence in sentences:
        current_len = sum(len(s.split()) for s in current_chunk)
        if current_len + len(sentence.split()) < max_chunk_words:
            current_chunk.append(sentence)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    # Step 3: Summarize each chunk
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
        summaries.append(summary)

    # Step 4: Combine summaries
    final_summary = " ".join(summaries)
    return final_summary

# Summarize Tool
class SummarizeTool(BaseTool):
    name: str = "Large Text Summarizer"
    description: str = "Summarizes long text into a concise summary using BART and spaCy."

    def _run(self, text: str) -> str:
        try:
            return summarize_large_text(text)
        except Exception as e:
            return f"Error summarizing text: {str(e)}"

# summarize_tool = Tool(
#     name="summarize_tool",
#     description="Summarizes a long text into a concise summary. Input should be a long text.",
#     func=summarize_large_text
# )


#summary into blog
