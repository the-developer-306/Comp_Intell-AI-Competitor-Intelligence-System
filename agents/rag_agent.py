import os
from tools.rag_tools import load_documents, split_documents, build_vectorstore
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub
import streamlit as st
import warnings
warnings.filterwarnings('ignore')

def generate_company_context(file_paths: list) -> str:
    documents = load_documents(file_paths)
    split_docs = split_documents(documents)
    vectorstore = build_vectorstore(split_docs)

    # Note: This stage doesn't use DeepSeek yet.
    # We're only retrieving relevant chunks from internal docs.
    # These chunks will be passed as context to DeepSeek later for final generation.

    retriever = vectorstore.as_retriever(search_type="similarity", k=5)

    questions = [
        "What products or services does the company offer?",
        "What is its mission or vision?",
        "What technical strengths does it have?",
        "Who is the target audience?",
        "What are the current challenges or opportunities?"
    ]

    context_chunks = []
    for question in questions:
        results = retriever.get_relevant_documents(question)
        answer = "\n".join([doc.page_content for doc in results])
        context_chunks.append(f"**Q:** {question}\n**A:**\n{answer}\n")

    return "\n\n".join(context_chunks)
