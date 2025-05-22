import streamlit as st
import os
import random
import re
from langchain_google_genai import ChatGoogleGenerativeAI

def quiz_interface():
    """Interface for the quiz generation functionality"""
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    
    st.subheader("📝 Generate Quiz from Your Documents")
    
    # Quiz generation options
    col1, col2 = st.columns(2)
    
    with col1:
        num_questions = st.slider("Number of Questions", min_value=3, max_value=10, value=5, step=1)
    
    with col2:
        difficulty = st.select_slider(
            "Difficulty Level",
            options=["Easy", "Medium", "Hard"],
            value="Medium"
        )
    
    # Generate button
    if st.button("🧠 Generate Quiz"):
        generate_quiz(num_questions, difficulty)
    
    # Display quiz if available
    if st.session_state.quiz_questions:
        display_quiz()
    
    st.markdown('</div>', unsafe_allow_html=True)

def generate_quiz(num_questions, difficulty):
    """Generate MCQ quiz questions based on document content"""
    # Check if documents have been processed
    if st.session_state.processed_files == 0:
        st.warning("Please process documents first before generating a quiz.")
        return
    
    try:
        with st.spinner(f"Generating {num_questions} {difficulty.lower()}-level questions..."):
            # Get API key
            api_key = os.getenv("GOOGLE_API_KEY")
            
            # Create the model
            model = ChatGoogleGenerativeAI(
                model="models/gemini-1.5-flash",
                temperature=0.7,
                google_api_key=api_key
            )
            
            # Create the prompt
            prompt = f"""
            Generate {num_questions} multiple-choice questions (MCQs) based on the content of the document.
            
            Difficulty level: {difficulty}
            
            For each question:
            1. Create a clear question related to important concepts in the document
            2. Provide 4 possible answers (A, B, C, D)
            3. Only ONE answer should be correct
            4. Mark the correct answer with a * at the beginning
            
            Format each question exactly like this example:
            
            Q1: What is the capital of France?
            A) Berlin
            B) Madrid
            C) *Paris
            D) Rome
            
            Make sure each question is distinct, relevant, and tests understanding rather than just memory.
            """
            
            # Load the vector store to access document content
            from utils import get_pdf_text
            
            # Get text from PDFs (assuming PDFs are stored in session state)
            if hasattr(st.session_state, 'pdf_content'):

                
                from io import BytesIO
                pdf_file = BytesIO(st.session_state.pdf_content)
                content = get_pdf_text([pdf_file])
                
                # Limit content length for API
                max_length = 50000
                if len(content) > max_length:
                    content = content[:max_length]
                
                # Add content to prompt
                full_prompt = prompt + "\n\nDocument content (extract):\n" + content
                
                # Generate questions
                response = model.invoke(full_prompt)
                quiz_text = response.content
                
                # Extract questions and answers
                process_quiz_response(quiz_text)
            else:
                st.error("Cannot access PDF content. Please re-upload a single PDF file.")
    
    except Exception as e:
        st.error(f"Error generating quiz: {str(e)}")

def process_quiz_response(quiz_text):
    """Process the quiz response from the AI"""
    # Extract questions and options
    questions = []
    answers = []
    
    # Use regex to extract questions and options
    pattern = r'Q\d+: (.*?)\nA\) (.*?)\nB\) (.*?)\nC\) (.*?)\nD\) (.*?)(?=\n\n|\Z)'
    matches = re.findall(pattern, quiz_text, re.DOTALL)
    
    for match in matches:
        question = match[0].strip()
        options = [match[1].strip(), match[2].strip(), match[3].strip(), match[4].strip()]
        
        # Find the correct answer (marked with *)
        correct_index = None
        for i, option in enumerate(options):
            if option.startswith('*'):
                options[i] = option[1:].strip()  # Remove the * marker
                correct_index = i
                break
        
        # If no correct answer was marked, choose randomly (fallback)
        if correct_index is None:
            correct_index = random.randint(0, 3)
        
        questions.append({
            'question': question,
            'options': options
        })
        
        answers.append(correct_index)
    
    # Save to session state
    st.session_state.quiz_questions = questions
    st.session_state.quiz_answers = answers
    st.session_state.user_answers = [-1] * len(questions)  # Initialize with no selection
    
    st.success(f"✅ Generated {len(questions)} questions!")

def display_quiz():
    """Display the quiz questions and options"""
    st.subheader("📋 Quiz Questions")
    
    # Check if we have questions
    if not st.session_state.quiz_questions:
        st.warning("No quiz questions available. Please generate a quiz first.")
        return
    
    # Display each question
    for i, q in enumerate(st.session_state.quiz_questions):
        st.markdown(f"""
        <div class="quiz-question">
            <div class="question-header">Question {i+1}</div>
            <div class="question-text">{q['question']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Radio button for options
        selected = st.radio(
            f"Select your answer for question {i+1}:",
            options=q['options'],
            index=st.session_state.user_answers[i] if st.session_state.user_answers[i] >= 0 else None,
            key=f"q{i}",
            label_visibility="collapsed"
        )
        
        # Save the selection
        if selected:
            option_index = q['options'].index(selected)
            st.session_state.user_answers[i] = option_index
        
        st.markdown("---")
    
    # Submit button
    if st.button("📊 Submit Quiz"):
        score = calculate_score()
        display_score(score)

def calculate_score():
    """Calculate the quiz score"""
    correct = 0
    total = len(st.session_state.quiz_answers)
    
    for i, (user, correct_ans) in enumerate(zip(st.session_state.user_answers, st.session_state.quiz_answers)):
        if user == correct_ans:
            correct += 1
    
    return {
        'correct': correct,
        'total': total,
        'percentage': round((correct / total) * 100) if total > 0 else 0
    }

def display_score(score):
    """Display the quiz score"""
    st.markdown(f"""
    <div class="score-display">
        <div class="score-number">{score['percentage']}%</div>
        <div class="score-label">{score['correct']} correct out of {score['total']} questions</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show correct answers
    st.subheader("📝 Answer Key")
    
    for i, (question, correct_idx) in enumerate(zip(st.session_state.quiz_questions, st.session_state.quiz_answers)):
        user_idx = st.session_state.user_answers[i]
        
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <b>Question {i+1}:</b> {question['question']}<br>
            <b>Correct answer:</b> {question['options'][correct_idx]}<br>
            <b>Your answer:</b> {question['options'][user_idx] if user_idx >= 0 else "Not answered"}<br>
            <b>Result:</b> {"✅ Correct" if user_idx == correct_idx else "❌ Incorrect"}
        </div>
        """, unsafe_allow_html=True)