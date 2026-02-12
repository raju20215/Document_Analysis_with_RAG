# -------------------------------------------------------------
# first.py — Build Vector DB + Load RAG Pipeline (LangChain 0.2.x)
# -------------------------------------------------------------

import os
import sys
import json

# Document loaders
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import Docx2txtLoader

# Text splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Embeddings + VectorDB
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# LLM + Prompt + Chain (Modern LCEL API)
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


# -------------------------------------------------------------
# CONFIG PATHS
# -------------------------------------------------------------
DATA_PATH = "files"       # folder where PDFs are placed
DB_PATH = "vectordb"      # folder where FAISS DB is saved

# Model configuration - change these to use different models
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gemma3:1b")  # Using gemma3:1b as default


# -------------------------------------------------------------
# BUILD VECTOR DB FROM PDFs (RUN ONLY ONCE)
# -------------------------------------------------------------
def build_vector_database():

    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        print(f"[WARNING] Created folder: {DATA_PATH}")
        print("[INFO] Add PDF files and run again.")
        sys.exit()

    # Get all supported files (PDF and DOCX)
    pdf_files = [f for f in os.listdir(DATA_PATH) if f.lower().endswith(".pdf")]
    docx_files = [f for f in os.listdir(DATA_PATH) if f.lower().endswith(".docx")]
    all_files = pdf_files + docx_files

    if not all_files:
        print(f"[WARNING] No PDF or DOCX files found in {DATA_PATH}")
        sys.exit()

    print(f"[INFO] Loading documents... (PDFs: {len(pdf_files)}, DOCX: {len(docx_files)})")
    documents = []

    # Process PDF files with PyMuPDF
    for file in pdf_files:
        file_path = os.path.join(DATA_PATH, file)
        try:
            print(f"[INFO] Processing PDF: {file}")
            loader = PyMuPDFLoader(file_path)
            pages = loader.load()

            for page in pages:
                text_lower = page.page_content.lower()

                # simple metadata classification
                if "leave" in text_lower:
                    page.metadata["policy_type"] = "leave_policy"
                elif "privacy" in text_lower or "speak up" in text_lower:
                    page.metadata["policy_type"] = "privacy_policy"
                else:
                    page.metadata["policy_type"] = "general_policy"

                page.metadata["source"] = file
                page.metadata["file_type"] = "pdf"
                documents.append(page)
            
            print(f"[SUCCESS] Loaded {len(pages)} pages from {file}")
        except Exception as e:
            print(f"[ERROR] Failed to load {file}: {str(e)}")
            print(f"[INFO] Skipping {file} and continuing...")
            continue
    
    # Process DOCX files
    for file in docx_files:
        file_path = os.path.join(DATA_PATH, file)
        try:
            print(f"[INFO] Processing DOCX: {file}")
            loader = Docx2txtLoader(file_path)
            docs = loader.load()

            for doc in docs:
                text_lower = doc.page_content.lower()

                # simple metadata classification
                if "leave" in text_lower:
                    doc.metadata["policy_type"] = "leave_policy"
                elif "privacy" in text_lower or "speak up" in text_lower:
                    doc.metadata["policy_type"] = "privacy_policy"
                else:
                    doc.metadata["policy_type"] = "general_policy"

                doc.metadata["source"] = file
                doc.metadata["file_type"] = "docx"
                doc.metadata["page"] = 1  # DOCX doesn't have page numbers
                documents.append(doc)
            
            print(f"[SUCCESS] Loaded {file}")
        except Exception as e:
            print(f"[ERROR] Failed to load {file}: {str(e)}")
            print(f"[INFO] Skipping {file} and continuing...")
            continue

    print(f"[INFO] Total pages loaded: {len(documents)}")

    # 2. Split into chunks
    print("[INFO] Splitting pages...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)
    print(f"[INFO] Chunks created: {len(chunks)}")
    
    # Validate chunks
    if not chunks:
        print("[ERROR] No text content found in PDFs. Please add PDFs with text content.")
        sys.exit()

    # 3. Embeddings
    print(f"[INFO] Loading embedding model ({EMBEDDING_MODEL})...")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    # 4. Save FAISS DB
    print("[INFO] Building FAISS vector database...")
    vectordb = FAISS.from_documents(chunks, embeddings)
    vectordb.save_local(DB_PATH)

    print(f"[SUCCESS] Vector DB saved to: {DB_PATH}")


# -------------------------------------------------------------
# LOAD VECTOR DB + BUILD RAG PIPELINE (Modern LCEL API)
# -------------------------------------------------------------
def load_rag_pipeline():

    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    vectordb = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 5})

    llm = ChatOllama(model=CHAT_MODEL)

    # Modern ChatPromptTemplate for LCEL
    prompt = ChatPromptTemplate.from_template("""
You are an expert document analyst and information retrieval specialist. Your core competencies include:

1. **Precision Search**: Expertly searching through documents to find relevant information
2. **Information Extraction**: Accurately extracting facts, figures, and key details from documents
3. **Clear Communication**: Explaining information in a clear, well-structured, and easy-to-understand manner
4. **Contextual Understanding**: Understanding the context and providing complete, relevant answers

Your task is to analyze the provided context and answer the user's question with:
- Accuracy: Only use information from the provided documents
- Clarity: Explain concepts clearly and thoroughly
- Completeness: Provide all relevant details from the context
- Structure: Use bullet points, numbers, or paragraphs as appropriate

If information is not available in the documents, clearly state: "This information is not available in the provided documents."

Context:
{context}

Question:
{question}

Provide a clear, detailed, and well-explained answer:
""")

    # Helper function to format documents
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Modern LCEL chain that returns both answer and source documents
    from langchain_core.runnables import RunnableParallel, RunnableLambda
    
    # Create the answer generation chain
    answer_chain = (
        RunnableLambda(lambda x: {"context": format_docs(x["context"]), "question": x["question"]})
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # Combine retrieval and answer generation
    rag_chain = RunnableParallel(
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
    ).assign(answer=answer_chain)

    return rag_chain


# -------------------------------------------------------------
# Run indexer directly
# -------------------------------------------------------------
if __name__ == "__main__":
    build_vector_database()
