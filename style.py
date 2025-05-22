import streamlit as st

def inject_custom_css():
    """Inject custom CSS styling for the application"""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Main app styling */
        .main {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        /* Header styling */
        .main-header {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .main-header h1 {
            color: #2d3748;
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .main-header p {
            color: #718096;
            font-size: 1.1rem;
            margin-bottom: 0;
            font-weight: 400;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
            background: white;
            border-radius: 15px;
            padding: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 60px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 10px;
            color: #667eea;
            font-weight: 600;
            font-size: 16px;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
        }
        
        /* Chat container styling */
        .chat-container, .quiz-container {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        /* Question input styling */
        .stTextInput > div > div > input {
            border-radius: 15px;
            border: 2px solid #e2e8f0;
            padding: 1rem;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: #f8fafc;
            color: #2d3748 !important;
            font-family: 'Inter', sans-serif;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            background: white;
            color: #2d3748 !important;
        }
        
        /* Quiz question styling */
        .quiz-question {
            background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .question-header {
            color: #667eea;
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }
        
        .question-text {
            color: #2d3748;
            line-height: 1.6;
            font-size: 1rem;
            white-space: pre-line;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #f8fafc 0%, #edf2f7 100%);
        }
        
        .sidebar-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .sidebar-header h2 {
            margin: 0;
            font-weight: 600;
            font-size: 1.5rem;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 15px;
            padding: 0.8rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            width: 100%;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        /* Response styling */
        .response-container {
            background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .response-label {
            color: #667eea;
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }
        
        .response-text {
            color: #2d3748;
            line-height: 1.6;
            font-size: 1rem;
        }
        
        /* Stats cards */
        .stats-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s ease;
        }
        
        .stats-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }
        
        .stats-number {
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 0.5rem;
        }
        
        .stats-label {
            color: #718096;
            font-weight: 500;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.5px;
        }
        
        /* Score display */
        .score-display {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        
        .score-number {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .score-label {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)