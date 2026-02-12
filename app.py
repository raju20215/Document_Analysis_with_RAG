import streamlit as st
import os
import tempfile
import shutil
from first import build_vector_database, load_rag_pipeline

st.set_page_config(page_title="DocGenius AI", page_icon="📘", layout="wide")

st.title("📘 DocGenius — Local Document Q&A")
st.caption("AI Document Assistant (100% Private, Offline, Powered by Ollama + LangChain)")


# ---------------------------------------------------
# FILE UPLOAD SECTION
# ---------------------------------------------------
with st.sidebar:
    st.header("📁 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF or Word documents",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        help="Upload PDF files (including scanned documents with images) or Word documents (.docx)"
    )
    
    if uploaded_files:
        if st.button("🔨 Build Vector Database", type="primary"):
            # Save uploaded files to the files directory
            if not os.path.exists("files"):
                os.makedirs("files")
            
            # Clear existing files
            for f in os.listdir("files"):
                if f.endswith((".pdf", ".docx")):
                    os.remove(os.path.join("files", f))
            
            # Save uploaded files
            with st.spinner("Saving uploaded files..."):
                for uploaded_file in uploaded_files:
                    file_path = os.path.join("files", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                st.success(f"✅ Saved {len(uploaded_files)} file(s)")
            
            # Build vector database
            try:
                with st.spinner("Building vector database... This may take a few minutes."):
                    # Remove old vector DB
                    if os.path.exists("vectordb"):
                        shutil.rmtree("vectordb")
                    
                    # Build new vector DB
                    build_vector_database()
                    st.success("✅ Vector database created successfully!")
                    st.info("Please refresh the page to start chatting with your documents.")
            except Exception as e:
                import traceback
                st.error(f"❌ Error building database: {str(e)}")
                with st.expander("🔍 View Full Error Details"):
                    st.code(traceback.format_exc())
    
    st.divider()
    st.caption("💡 **Tip:** Upload PDFs with readable text content for best results.")


# ---------------------------------------------------
# CHECK IF VECTOR DB EXISTS
# ---------------------------------------------------
DB_PATH = "vectordb"
if not os.path.exists(DB_PATH) or not os.path.exists(os.path.join(DB_PATH, "index.faiss")):
    st.warning("⚠️ No vector database found!")
    st.info("""
    **Get Started:**
    
    1. **Upload PDF files** using the sidebar on the left
    2. **Click "Build Vector Database"** to process your documents
    3. **Start chatting** with your documents!
    
    **Note:** Make sure Ollama is running with the required models:
    - `nomic-embed-text` (embeddings) - or set EMBEDDING_MODEL env variable
    - `gemma3:1b` (chat) - or set CHAT_MODEL env variable
    """)
    st.stop()


# ---------------------------------------------------
# LOAD RAG PIPELINE (VECTOR DB + RETRIEVER + LLM)
# ---------------------------------------------------
@st.cache_resource
def load_pipeline():
    return load_rag_pipeline()

try:
    rag_chain = load_pipeline()
    st.success("✅ Vector DB loaded. You can now chat with your documents.")
except Exception as e:
    st.error(f"❌ Error loading RAG pipeline: {str(e)}")
    st.info("Please make sure Ollama is running and the required models are installed.")
    st.stop()


# ---------------------------------------------------
# SIDEBAR - DATABASE MANAGEMENT
# ---------------------------------------------------
with st.sidebar:
    st.divider()
    st.subheader("🗄️ Database Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.button("💣 Delete DB", type="secondary", use_container_width=True):
            if os.path.exists("vectordb"):
                shutil.rmtree("vectordb")
                st.success("Vector database deleted!")
                st.info("Please refresh the page.")
                st.cache_resource.clear()
                st.stop()


# ---------------------------------------------------
# CHAT INTERFACE
# ---------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history first (before input)
for msg_idx, entry in enumerate(st.session_state.chat_history):
    role = entry["role"]
    message = entry["content"]
    sources = entry.get("sources")
    
    if role == "user":
        st.chat_message("user").write(message)
    else:
        with st.chat_message("assistant"):
            st.write(message)
            
            # Display sources if available
            if sources:
                with st.expander("📚 View Sources", expanded=False):
                    for idx, doc in enumerate(sources, 1):
                        source_file = doc.metadata.get("source", "Unknown")
                        policy_type = doc.metadata.get("policy_type", "general")
                        page_num = doc.metadata.get("page", "N/A")
                        
                        st.markdown(f"**Source {idx}:** `{source_file}` (Page {page_num})")
                        st.markdown(f"**Type:** {policy_type}")
                        
                        # Show snippet of the source text
                        snippet = doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
                        st.text_area(
                            f"Content Preview {idx}",
                            snippet,
                            height=100,
                            key=f"history_msg{msg_idx}_source{idx}",
                            disabled=True
                        )
                        
                        if idx < len(sources):
                            st.divider()

# Chat input at the bottom
user_question = st.chat_input("Ask a question based on your documents...")

if user_question:
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user", 
        "content": user_question, 
        "sources": None
    })
    
    # Display user message immediately
    st.chat_message("user").write(user_question)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = rag_chain.invoke(user_question)
            answer = result["answer"]
            sources = result["context"]
        
        # Display answer
        st.write(answer)
        
        # Display sources
        if sources:
            with st.expander("📚 View Sources", expanded=False):
                for idx, doc in enumerate(sources, 1):
                    source_file = doc.metadata.get("source", "Unknown")
                    policy_type = doc.metadata.get("policy_type", "general")
                    page_num = doc.metadata.get("page", "N/A")
                    
                    st.markdown(f"**Source {idx}:** `{source_file}` (Page {page_num})")
                    st.markdown(f"**Type:** {policy_type}")
                    
                    snippet = doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
                    st.text_area(
                        f"Content Preview {idx}",
                        snippet,
                        height=100,
                        key=f"new_msg{len(st.session_state.chat_history)}_source{idx}",
                        disabled=True
                    )
                    
                    if idx < len(sources):
                        st.divider()
    
    # Add assistant message to history
    st.session_state.chat_history.append({
        "role": "assistant", 
        "content": answer,
        "sources": sources
    })
    
    # Rerun to update the display
    st.rerun()
