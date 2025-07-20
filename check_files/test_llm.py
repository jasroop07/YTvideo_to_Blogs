import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

print("Attempting to load environment variables...")
load_dotenv()

# 1. Check if the API key is loaded
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("🔴 ERROR: GOOGLE_API_KEY not found in environment variables.")
    print("   Please make sure your .env file is in the correct directory and contains the line:")
    print("   GOOGLE_API_KEY='Your_API_Key_Here'")
else:
    print(f"✅ API Key loaded successfully. The key starts with: {api_key[:4]}...")

# 2. Try to initialize the LLM
try:
    print("\nAttempting to initialize the ChatGoogleGenerativeAI model...")
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key
    )
    print("✅ LLM initialized successfully.")
except Exception as e:
    print(f"🔴 ERROR: Failed to initialize the LLM. Error: {e}")
    # Exit if initialization fails
    exit()

# 3. Try to make a simple API call
try:
    print("\nAttempting to make a test call to the Gemini API...")
    response = llm.invoke("Hello, what is the capital of France?")
    print("✅ API call successful!")
    print("\nResponse from Gemini:")
    print(response.content)
except Exception as e:
    print(f"🔴 ERROR: The API call failed. This is likely the source of your problem in CrewAI.")
    print(f"   Error details: {e}")

