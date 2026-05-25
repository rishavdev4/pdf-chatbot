 # 📄 GenAI PDF Chatbot

A RAG-based PDF chatbot that lets you upload any PDF and ask questions about it using AI.

## 🚀 Built With
- **LangChain** — Document loading and text splitting
- **Groq API** — Free LLaMA3 model for answering questions
- **Streamlit** — Interactive web interface
- **Python** — Core language

## ⚙️ How It Works
1. Upload any PDF file
2. The PDF is split into text chunks
3. Your question + PDF content is sent to LLaMA3
4. AI answers based on the document

## 🛠️ Setup & Run
```bash
pip install streamlit langchain-community langchain-text-splitters langchain-groq pypdf
python -m streamlit run app.py
```

## 📸 Demo
Upload a PDF → Ask questions → Get instant AI answers

## 🔑 Requirements
- Free Groq API key from [console.groq.com](https://console.groq.com)
