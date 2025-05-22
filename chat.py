import streamlit as st
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import time

def chat_interface():
    """Interface for the PDF chatbot functionality"""
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Chat input
    st.subheader("💬 Ask questions about your documents")
    
    # Get user question
    user_question = st.text_input(
        "Enter your question:",
        placeholder="Ask something about your uploaded PDFs...",
        key="chat_input",
        label_visibility="collapsed"
    )
    
    # Process the question
    if user_question:
        handle_user_question(user_question)
    
    # Chat history
    if st.session_state.chat_history:
        st.subheader("💭 Chat History")
        
        # Display messages in reverse chronological order
        for i, (question, answer) in enumerate(reversed(st.session_state.chat_history)):
            # Answer box
            st.markdown(f"""
            <div class="response-container">
                <div class="response-label">🤖 AI Assistant:</div>
                <div class="response-text">{answer}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Question box (smaller)
            st.markdown(f"""
            <div style="background: #f1f5f9; padding: 0.8rem; border-radius: 10px; font-size: 0.9rem; color: #475569; margin-bottom: 1rem;">
                <b>❓ You asked:</b> {question}
            </div>
            """, unsafe_allow_html=True)
    
    # Display stats
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{st.session_state.processed_files}</div>
            <div class="stats-label">Documents Processed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{st.session_state.total_chunks}</div>
            <div class="stats-label">Text Chunks</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def handle_user_question(user_question):
    """Process user question and generate response"""
    from utils import get_conversational_chain
    
    # Check if documents have been processed
    if st.session_state.processed_files == 0:
        st.warning("Please process documents first before asking questions.")
        return
    
    try:
        with st.spinner("Thinking..."):
            # Slight delay for better UX
            time.sleep(0.5)
            
            # Get API key
            api_key = os.getenv("GOOGLE_API_KEY")
            
            # Initialize embeddings
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=api_key
            )
            
            # Load the vector store
            vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
            
            # Search for similar documents
            docs = vector_store.similarity_search(user_question)
            
            # Get the conversational chain
            chain = get_conversational_chain(api_key)
            
            # Generate response
            response = chain(
                {"input_documents": docs, "question": user_question},
                return_only_outputs=True
            )
            
            # Save to chat history
            st.session_state.chat_history.append((user_question, response["output_text"]))
            
            # Display the response
            st.markdown(f"""
            <div class="response-container">
                <div class="response-label">🤖 AI Assistant:</div>
                <div class="response-text">{response["output_text"]}</div>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error processing your question: {str(e)}")
        if "faiss_index" not in os.listdir():
            st.warning("No documents have been processed. Please upload and process documents first.")