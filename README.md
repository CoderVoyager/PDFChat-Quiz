# 📚 PDF AI Assistant & Quiz Generator

PDF AI Assistant & Quiz Generator is a Streamlit-based application that allows users to interact with PDF documents using AI. It provides two main functionalities: chatting with PDFs to extract insights and generating multiple-choice quizzes to test knowledge. Powered by Google Gemini AI and LangChain, this app is ideal for students, educators, and professionals.

---

## ✨ Features

* 📤 **Multiple PDF Upload**: Upload and process multiple PDF files simultaneously.
* 💬 **Chat with PDFs**: Ask questions and get detailed, context-aware answers from your documents.
* 📝 **Quiz Generation**: Generate multiple-choice quizzes from PDF content.
* 🎯 **Difficulty Levels**: Choose quiz difficulty (Easy, Medium, Hard).
* 📊 **Instant Scoring**: Get immediate feedback and answer explanations.
* 🔒 **Secure**: All processing is done locally, ensuring your data remains private.

---

## 🚀 Quick Start

1. **Clone the Repository**

   ```bash
   git clone https://github.com/CoderVoyager/PDFChat-Quiz.git
   cd PDFChat-Quiz
   ```
2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```
3. **Set Up Google Gemini API Key**

   * Create a `.env` file in the root directory.
   * Add your API key like this:

     ```env
     GEMINI_API_KEY=your_api_key_here
     ```
4. **Run the App**

   ```bash
   streamlit run app_2.py
   ```

---

## 🖥️ Usage

1. **Upload PDFs** using the sidebar.
2. Click **"Process Documents"** to embed content.
3. Go to **Chat** tab and ask questions.
4. Go to **Quiz** tab to generate and take a quiz.

---

## 🧰 Tech Stack

* **Frontend**: Streamlit
* **AI Model**: Google Gemini
* **Vector Store**: FAISS
* **PDF Parsing**: PyPDF2
* **RAG Architecture**: LangChain

---

## 📂 Project Structure

```
├── app_2.py            # Main Streamlit app
├── chat.py             # Chat functionality
├── quiz.py             # Quiz generation and scoring
├── utils.py            # Utility functions (PDF parsing, vector store, etc.)
├── style.py            # Custom CSS for beautiful UI
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## ⚙️ How It Works

1. **Document Ingestion**: PDFs are parsed and split into chunks.
2. **Embedding**: Chunks are embedded using Google Gemini and stored in FAISS.
3. **Chat**: Questions are matched with chunks and answered by Gemini.
4. **Quiz Generation**: Gemini creates MCQs based on extracted content.



