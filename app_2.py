import streamlit as st
from utils import setup_environment
from chat import chat_interface
from quiz import quiz_interface
from style import inject_custom_css

# Set up page and environment
st.set_page_config(
    page_title="PDF AI Assistant & Quiz Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)
setup_environment()
inject_custom_css()

# Initialize session state
for key, default in {
    "processed_files": 0, "total_chunks": 0, "chat_history": [],
    "quiz_questions": [], "quiz_answers": [], "user_answers": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Header
st.markdown('<div class="main-header"><h1>📚 PDF AI Assistant & Quiz Generator</h1><p>Upload PDF documents, chat with them, and generate interactive quizzes</p></div>', unsafe_allow_html=True)

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["💬 Chat with PDF", "📝 Generate Quiz"])

with tab1:
    chat_interface()

with tab2:
    quiz_interface()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2>🔧 Document Manager</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    st.markdown("### 📁 Upload Documents")
    pdf_docs = st.file_uploader(
        "", 
        accept_multiple_files=True,
        type=["pdf"],
        help="Upload one or more PDF files to get started",
        label_visibility="collapsed"
    )
    
    if pdf_docs:
        st.success(f"✅ {len(pdf_docs)} file(s) selected")
        for pdf in pdf_docs:
            st.write(f"📄 {pdf.name}")
        
        # Store PDF content for quiz generation
        if len(pdf_docs) == 1:
            st.session_state.pdf_content = pdf_docs[0].getbuffer()
    
    from utils import process_documents, clear_data
    
    # Process button
    if st.button("🚀 Process Documents"):
        process_documents(pdf_docs)
    
    # Clear button
    if st.button("🗑️ Clear All Data"):
        clear_data()
    
    # About section
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This app combines **PDF chatbot** and **quiz generation** features using **Google's Gemini AI**.
    
    **Features:**
    - 📤 Multiple PDF upload
    - 💬 Chat with PDFs
    - 📝 Generate MCQ quizzes
    - 🎯 Multiple difficulty levels
    - 📊 Instant scoring
    
    **Built with:**
    - Streamlit
    - LangChain
    - Google Gemini AI
    - FAISS Vector Store
    """)

if __name__ == "__main__":
    pass  # Main logic is handled in the imports and tab layout