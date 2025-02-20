import streamlit as st
import fitz  # PyMuPDF for PDF processing
import docx  # For .docx processing
import os
from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter

# --- UI/UX IMPROVEMENTS ---
st.set_page_config(page_title="DocuQuery AI", page_icon="📄", layout="wide")

st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>📄 DocuQuery AI</h1>
    <p style='text-align: center; font-size: 18px; color: gray;'>
        Upload <b>PDF, DOCX, or TXT files</b> and ask questions to retrieve relevant information.
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# --- FILE UPLOADER ---
uploaded_files = st.file_uploader(
    "Upload Documents (Multiple Supported)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

question = st.text_input("🔍 Enter your question:", placeholder="Type your query here...")

def extract_text_from_pdfs(uploaded_files):
    extracted_texts = []
    for file in uploaded_files:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            text = "\n".join([page.get_text() for page in doc])
            extracted_texts.append(text)
    return extracted_texts

def extract_text_from_docx(uploaded_files):
    extracted_texts = []
    for file in uploaded_files:
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        extracted_texts.append(text)
    return extracted_texts

def extract_text_from_txt(uploaded_files):
    extracted_texts = []
    for file in uploaded_files:
        text = file.read().decode("utf-8")
        extracted_texts.append(text)
    return extracted_texts

def extract_text_from_documents(uploaded_files):
    pdf_files = [file for file in uploaded_files if file.name.endswith(".pdf")]
    docx_files = [file for file in uploaded_files if file.name.endswith(".docx")]
    txt_files = [file for file in uploaded_files if file.name.endswith(".txt")]

    extracted_texts = extract_text_from_pdfs(pdf_files)
    extracted_texts += extract_text_from_docx(docx_files)
    extracted_texts += extract_text_from_txt(txt_files)

    return extracted_texts

def process_documents(uploaded_files, question):
    if not uploaded_files:
        return "No documents uploaded."

    model_local = Ollama(model="mistral")
    extracted_texts = extract_text_from_documents(uploaded_files)

    if not extracted_texts:
        return "No text extracted from documents."

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    doc_splits = text_splitter.create_documents(extracted_texts)

    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text'),
        persist_directory="./chroma_db"
    )
    vectorstore.persist()

    retriever = vectorstore.as_retriever()
    retrieved_docs = retriever.invoke(question)
    context_text = "\n".join([doc.page_content for doc in retrieved_docs])

    if not context_text.strip():
        return "No relevant information found in the uploaded documents."

    after_rag_template = """Answer the question based only on the following context:
    {context}
    Question: {question}
    """
    after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)

    inputs = {"context": context_text, "question": question}
    after_rag_chain = after_rag_prompt | model_local | StrOutputParser()

    return after_rag_chain.invoke(inputs)

# --- QUERY DOCUMENTS ---
if st.button("Query Documents", use_container_width=True):
    with st.spinner("Processing..."):
        answer = process_documents(uploaded_files, question)
        if not answer.strip():
            answer = "No relevant information found in the uploaded documents."

        st.text_area("Answer", value=answer, height=300, disabled=True)
