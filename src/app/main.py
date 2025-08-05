from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Define a request model for incoming chat queries
class ChatRequest(BaseModel):
    user_input: str

app = FastAPI()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")

# Define the chat prompt template
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant whose only task is to help human by answering the question asked by him."),
    ("assistant", "How can I help you?"),
    ("human", "{user_input}"),
])

@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    """
    Handles chat requests, processes user input through an LLM, and returns the AI's response.
    """
    try:

        chain = chat_template | llm
        response = chain.invoke({"user_input": request.user_input})
        return {"answer": response.content}
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}, 500
