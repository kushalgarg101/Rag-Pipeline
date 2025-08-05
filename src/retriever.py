from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from typing import List, Optional
from dotenv import load_dotenv
from prompt_temp import PROMPT_TEMPLATE
from langchain_google_genai import ChatGoogleGenerativeAI
import os

class Retreiver:
    def __init__(self, query_text):
        self.query_text = query_text
        self.embed_func = FastEmbedEmbeddings()
        self.db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embed_func)
        self.results =  self.db.similarity_search_with_score(self.query_text, k=3)

    def response(self):
        self.retrieved_context = "\n\n '---'*100 \n\n".join([doc.page_content for doc, _ in self.results])
        prompt_temp = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_temp.format(context=self.retrieved_context, question=self.query_text)
    
        llm = ChatGoogleGenerativeAI( model="gemini-2.5-pro", temperature=0, max_tokens=None, timeout=None, max_retries=2)
        response_text = llm.invoke(prompt)
        sources = [doc.metadata.get("id", None) for doc, _score in self.results]
        format_response = f"Response: {response_text.content} \n\n Sources: {sources}"

        print(format_response)
        return response_text

if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    CHROMA_PATH = r"D:\End_to_End_RAG\Simple_Rag\src\Data"
    init_retrieve = Retreiver("Tell me about what context topics you are given")
    init_retrieve.response()