import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import time

def setup_environment():
    """Load environment variables and configure Google API"""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Google API key not found. Please add it to your .env file.")
        st.stop()
    
    genai.configure(api_key=api_key)
    return api_key

def get_pdf_text(pdf_docs):
    """Extract text from PDF documents"""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text, chunk_size=10000, chunk_overlap=200):
    """Split text into manageable chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(chunks, api_key):
    """Create vector embeddings and store in FAISS index"""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", 
        google_api_key=api_key
    )
    vector_store = FAISS.from_texts(chunks, embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

def get_conversational_chain(api_key):
    """Create a conversational chain for question answering"""
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",
        temperature=0.3,
        google_api_key=api_key
    )

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def process_documents(pdf_docs):
    """Process PDF documents to create vector store"""
    if not pdf_docs:
        st.warning("Please upload PDF documents first.")
        return
    
    with st.spinner("Processing documents..."):
        # Get API key
        api_key = os.getenv("GOOGLE_API_KEY")
        
        # Extract text from PDFs
        raw_text = get_pdf_text(pdf_docs)
        
        # Create text chunks
        text_chunks = get_text_chunks(raw_text)
        st.session_state.total_chunks = len(text_chunks)
        
        # Create vector store
        get_vector_store(text_chunks, api_key)
        
        st.session_state.processed_files = len(pdf_docs)
        
    st.success(f"✅ Successfully processed {len(pdf_docs)} documents with {len(text_chunks)} text chunks!")

def clear_data():
    """Clear all data and reset session state"""
    if os.path.exists("faiss_index"):
        import shutil
        try:
            shutil.rmtree("faiss_index")
        except Exception as e:
            st.error(f"Error clearing data: {str(e)}")
    
    # Reset session state
    st.session_state.processed_files = 0
    st.session_state.total_chunks = 0
    st.session_state.chat_history = []
    st.session_state.quiz_questions = []
    st.session_state.quiz_answers = []
    st.session_state.user_answers = []
    
    st.success("✅ All data has been cleared.")
    st.experimental_rerun()