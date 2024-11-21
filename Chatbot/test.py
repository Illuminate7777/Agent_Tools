import os
import streamlit as st
from langchain.storage import LocalFileStore
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import ChatMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langserve import RemoteRunnable
from Rodney import processed_data

def embed_file(file):  # Read the uploaded file content

    persistence_directory = "./CrewAI/Chatbot"
    content = file[0]
    if not isinstance(content, str):
            content = str(content)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", "(?<=\. )", " ", ""],
        length_function=len,
    )
    
    loader = Document(page_content=content)
    text_splitter = text_splitter
    docs = text_splitter.split_documents([loader])
    embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="mxbai-embed-large")
    vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory = persistence_directory)
    retriever = vectorstore.as_retriever()
    return retriever

file = processed_data

retriever = embed_file(file)