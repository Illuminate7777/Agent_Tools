import os
import streamlit as st
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
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


LANGSERVE_ENDPOINT = "http://localhost:8000/llm/c/N4XyA"


RAG_PROMPT_TEMPLATE = """Your name is Harrison, the field manager for Rodney Govens. Answer the questions kindly based on the context, and if you don't know, say that you don't know.
Question: {question} 
Context: {context} 
Answer:"""

st.set_page_config(page_title="Rodney Govens Chatbot", page_icon="💬")
st.title("Rodney Govens Chatbot")


def print_history():
    for msg in st.session_state.messages:
        st.chat_message(msg.role).write(msg.content)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        ChatMessage(role="Harisson", content="How can I help?")
    ]



def add_history(role, content):
    st.session_state.messages.append(ChatMessage(role=role, content=content))


def format_docs(docs):
    
    return "\n\n".join(doc.page_content for doc in docs)


def embed_file(file):  # Read the uploaded file content

    content = file[0]
    if not isinstance(content, str):
            content = str(content)

    cache_dir = LocalFileStore(f"./.cache/embeddings/embeddings")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", "(?<=\. )", " ", ""],
        length_function=len,
    )
    
    loader = Document(page_content=content)
    text_splitter = text_splitter
    docs = text_splitter.split_documents([loader])
    embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="mxbai-embed-large")
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
    vectorstore = Chroma.from_documents(documents=docs, embedding=cached_embeddings)
    retriever = vectorstore.as_retriever()
    return retriever


def format_docs(docs):
    
    return "\n\n".join(doc.page_content for doc in docs)

file = processed_data

retriever = embed_file(file)

print_history()


if user_input := st.chat_input():
    add_history("user", user_input)
    st.chat_message("user").write(user_input)
    with st.chat_message("assistant"):
        
        ollama = RemoteRunnable(LANGSERVE_ENDPOINT)
        chat_container = st.empty()
        if file is not None:
            prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

            
            rag_chain = (
                {
                    "context": retriever | format_docs,
                    "question": RunnablePassthrough(),
                }
                | prompt
                | ollama
                | StrOutputParser()
            )
            
            answer = rag_chain.stream(user_input)  
            chunks = []
            for chunk in answer:
                chunks.append(chunk)
                chat_container.markdown("".join(chunks))
            add_history("ai", "".join(chunks))
        else:
            prompt = ChatPromptTemplate.from_template(
                "Your name is Harrison, the field manager for Rodney Govens. Answer the questions kindly based on the context, and if you don't know, say that you don't know. Answer only this question :\n{input}"
            )

            # 체인을 생성합니다.
            chain = prompt | ollama | StrOutputParser()

            answer = chain.stream(user_input)  
            chunks = []
            for chunk in answer:
                chunks.append(chunk)
                chat_container.markdown("".join(chunks))
            add_history("ai", "".join(chunks))