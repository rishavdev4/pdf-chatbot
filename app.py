import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import tempfile
import os

st.set_page_config(page_title="GenAI PDF Chatbot", page_icon="📄")
st.title("📄 GenAI PDF Chatbot")
st.caption("Upload any PDF and ask questions — powered by Groq + LLaMA3")

with st.sidebar:
    st.header("⚙️ Setup")
    groq_api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")

if not groq_api_key:
    st.info("👈 Enter your Groq API key in the sidebar.")
    st.stop()

uploaded_file = st.file_uploader("📂 Upload your PDF", type="pdf")

if not uploaded_file:
    st.info("Please upload a PDF file to begin.")
    st.stop()

@st.cache_resource(show_spinner="Reading PDF...")
def process_pdf(file_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(file_bytes)
        temp_path = f.name
    loader = PyPDFLoader(temp_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(pages)
    os.unlink(temp_path)
    full_text = "\n\n".join([c.page_content for c in chunks])
    return full_text, len(pages)

full_text, num_pages = process_pdf(uploaded_file.read())
st.success(f"✅ PDF loaded! {num_pages} pages processed.")

llm = ChatGroq(api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

st.divider()
st.subheader("💬 Ask anything about your PDF")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Type your question here...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                prompt = f"""You are a helpful assistant. Answer the question based on the document below.

Document:
{full_text[:6000]}

Question: {question}

Answer:"""
                response = llm.invoke([HumanMessage(content=prompt)])
                answer = response.content
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {e}")