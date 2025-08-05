from prefect import task,flow,serve
from data import Pdfs_dir_loader
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from typing import List

# def main():
#     ini_loader = Pdfs_dir_loader(folder_path = r"D:\End_to_End_RAG\Simple_Rag\src\downloaded_pdfs")

#     @task
#     def data_chunk() -> PyPDFDirectoryLoader:
#         return ini_loader.docs
    
#     @task
#     def load_data_in_list() -> List:
#         return ini_loader.all_docs
    
#     @task
#     def chunk_clean(chunk_size: int, chunk_overlap: int) -> List:
#         return ini_loader.pdf_chunk_clean(chunk_size, chunk_overlap)
    
#     @task
#     def uniq_chunk_id(chunks: List) -> List:
#         return ini_loader.uniq_meta_data_for_chunk(chunks)
    
#     @task
#     def embedding_function() -> FastEmbedEmbeddings:
#         return ini_loader._embedding_func()

#     @task
#     def add_docs_to_vector_db(chunks: List) -> None:
#         ini_loader.vector_db_add(chunks,r"D:\End_to_End_RAG\Simple_Rag\src\Data")
#         return None

#     @flow
#     def data_load_to_db(chunk_size, chunk_overlap):
#         data_chunk()
#         load_data_in_list()
#         chunks = chunk_clean(chunk_size, chunk_overlap)
#         uniq_chunk_id(chunks)
#         embedding_function()
#         add_docs_to_vector_db(chunks)

#     return data_load_to_db(chunk_size = 500, chunk_overlap =100)

# instantiate your loader once
ini_loader = Pdfs_dir_loader(
    folder_path=r"D:\End_to_End_RAG\Simple_Rag\src\downloaded_pdfs"
)

@task
def data_chunk() -> PyPDFDirectoryLoader:
    return ini_loader.docs

@task
def load_data_in_list() -> List:
    return ini_loader.all_docs

@task
def chunk_clean(chunk_size: int, chunk_overlap: int) -> List:
    return ini_loader.pdf_chunk_clean(chunk_size, chunk_overlap)

@task
def uniq_chunk_id(chunks: List) -> List:
    return ini_loader.uniq_meta_data_for_chunk(chunks)

@task
def embedding_function() -> FastEmbedEmbeddings:
    return ini_loader._embedding_func()

@task
def add_docs_to_vector_db(chunks: List) -> None:
    ini_loader.vector_db_add(
        chunks,
        r"D:\End_to_End_RAG\Simple_Rag\src\Data"
    )

@flow(name="Simple_Rag")
def data_load_to_db(chunk_size = 500, chunk_overlap = 100):
    data_chunk()
    load_data_in_list()
    chunks = chunk_clean(chunk_size, chunk_overlap)
    uniq_chunk_id(chunks)
    embedding_function()
    add_docs_to_vector_db(chunks)

if __name__ == "__main__":
    data_load_to_db.serve(name="Simple_Rag", cron="5 * * * *")