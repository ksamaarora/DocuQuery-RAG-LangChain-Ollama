# DocuQuery RAG – LangChain & Ollama

**DocuQuery RAG** is a Retrieval-Augmented Generation (RAG) powered document query system that allows users to upload **PDF, DOCX, and TXT** files and retrieve relevant information by asking questions. The system leverages **LangChain, ChromaDB, and Ollama (Mistral model)** to provide efficient document indexing and query resolution.

## Demonstration

https://github.com/user-attachments/assets/cffd88a3-776d-4862-9b15-f3a48ac3d98b

If the video does not load, it can be accessed directly at [link]().

## Installation and Setup

### 1. Clone the Repository
To obtain a local copy of the project, execute the following command:

```bash
git clone https://github.com/ksamaarora/DocuQuery-RAG-LangChain-Ollama.git
cd DocuQuery-RAG-LangChain-Ollama
```

### 2. Install Dependencies
Ensure that **Python 3.8+** is installed. The required dependencies can be installed using:

```bash
pip install -r requirements.txt
```

### 3. Set Up Ollama
Ollama must be installed and running to execute the model. It can be downloaded from [Ollama's official website](https://ollama.ai/). Once installed, retrieve the **Mistral model** by executing:

```bash
ollama pull mistral
```

### 4. Run the Application
To run the application locally, open two separate terminals:

- **In the first terminal**, start the Ollama server:

  ```bash
  ollama serve
  ```

- **In the second terminal**, launch the Streamlit application:

  ```bash
  streamlit run streamlit_app.py
  ```

### Alternative Approach
This could have been implemented using Google's API key for document processing, but since it operates on a **pay-as-you-go** model, i have not used that implementation method. 

## Project Structure

```
DocuQuery-RAG-LangChain-Ollama
 ├── streamlit_app.py        # Main application script
 ├── requirements.txt        # Dependency list
 ├── chroma_db/              # Directory for document embeddings (ignored in Git)
 ├── README.md               # Project documentation
```

## Technologies Used

- **LangChain** – Framework for handling document processing and question answering.
- **ChromaDB** – Vector database for storing document embeddings.
- **Ollama (Mistral Model)** – Lightweight and efficient large language model.
- **Streamlit** – Web-based user interface framework.
- **PyMuPDF and python-docx** – Libraries for extracting text from PDF and DOCX files.
