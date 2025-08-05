from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from typing import List, Optional
from dotenv import load_dotenv
from prompt_temp import PROMPT_TEMPLATE
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel,Field
import os

def generate_answer(query_text: str = Field(..., min_length= 4)):
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    CHROMA_PATH = r"D:\End_to_End_RAG\Simple_Rag\src\Data"
    Embed_Func = FastEmbedEmbeddings()

    database = Chroma(persist_directory = CHROMA_PATH, embedding_function = Embed_Func)
    get_results = database.similarity_search_with_score(query_text, k=4)
    retrieved_context = "\n\n '----'*100 \n\n".join([doc.page_content for doc, _ in get_results])
    prompt_temp = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_temp.format(context = retrieved_context, question = query_text)

    llm = ChatGoogleGenerativeAI( model="gemini-2.5-pro", temperature=0, max_tokens=None, timeout=None, max_retries=2)
    response_text = llm.invoke(prompt)
    sources = [doc.metadata.get("id", None) for doc, _score in get_results]
    format_response = f"Response: {response_text.content} \n\n Sources: {sources}"

    return format_response



if __name__ == '__main__':
    generate_answer()