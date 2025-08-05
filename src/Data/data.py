import langchain
from langchain_core.documents import Document
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma
from typing import List, Optional
import os

class Pdfs_dir_loader:

    def __init__(self, folder_path: str):
        self.loader = PyPDFDirectoryLoader(folder_path)
        self.docs = self.loader.lazy_load()
        self.all_docs = []
        for doc in self.loader.lazy_load():
            self.all_docs.append(doc)
    
    @staticmethod
    def text_clean(texts):
        cleaned_text_docs = []
        for doc in texts:
            cleaned_content = doc.page_content.replace('\n', ' ')
            # cleaned_content = ' '.join(cleaned_content.split())
            # cleaned_content = cleaned_content.strip()
            cleaned_doc = Document(page_content=cleaned_content, metadata=doc.metadata)
            cleaned_text_docs.append(cleaned_doc)
        return cleaned_text_docs

    def pdf_chunk_clean(self, chunk_size: int, chunk_overlap: int):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
        )
        texts = text_splitter.split_documents(self.all_docs)
        cleaned_text = self.text_clean(texts)
        return cleaned_text

    def uniq_meta_data_for_chunk(self, chunks):
        last_page = None
        current_chunk_idx = 0
        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source} : {page}"
            if current_page_id == last_page:
                current_chunk_idx += 1
            else:
                current_chunk_idx = 0

            chunk_id = f"{current_page_id}:{current_chunk_idx}"
            last_page = current_page_id

            chunk.metadata["id"] = chunk_id

        return chunks
    
    def __embedding_func(self):
        embedding_function = FastEmbedEmbeddings()
        return embedding_function
    
    def vector_db_add(self, chunks):
        db = Chroma(persist_directory = CHROMA_PATH, embedding_function = self.__embedding_func())
        chunks_with_ids = self.uniq_meta_data_for_chunk(chunks)

        existing_items = db.get(include=[])
        existing_ids = set(existing_items["id"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")

        new_chunks = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks):
            print(f"👉 Adding new documents: {len(new_chunks)}")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
        else:
            print("✅ No new documents to add")

if __name__ == '__main__':
    CHROMA_PATH = r"D:\End_to_End_RAG\Simple_Rag\src\Data"
    pdf_folder = r"D:\End_to_End_RAG\Simple_Rag\src\downloaded_pdfs"
    init_pdf_loader = Pdfs_dir_loader(pdf_folder)
    # print(init_pdf_loader.all_docs[0])
    chunk_pdf = init_pdf_loader.pdf_chunk_clean(1000, 50)
    # print(chunk_pdf[0])
    uniq_chunk_id = init_pdf_loader.uniq_meta_data_for_chunk(chunk_pdf)
    # print(f"{uniq_chunk_id[0]}\n{'-' * 100}\n{uniq_chunk_id[1]}\n{'-' * 100}\n{uniq_chunk_id[2]}\n{'-' * 100}\n\
    #         {uniq_chunk_id[9]}\n{'-' * 100}\n{uniq_chunk_id[10]}\n{'-' * 100}\n{uniq_chunk_id[11]}")
    data_to_db = init_pdf_loader.vector_db_add(uniq_chunk_id)