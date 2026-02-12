# 📘 DocGenius - Local Document Q&A System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.2.x-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**AI Document Assistant - 100% Private, Offline, Powered by Ollama + LangChain**

</div>

---

## 🌟 Features

- **🔒 100% Private & Offline**: All processing happens locally on your machine. No data is sent to external servers.
- **📄 Multi-Format Support**: Upload and process PDF and Word (.docx) documents
- **🤖 AI-Powered Q&A**: Ask questions about your documents and get intelligent, context-aware answers
- **📚 Source Citations**: View the exact sources and page numbers used to generate each answer
- **🎨 User-Friendly Interface**: Built with Streamlit for a clean, intuitive experience
- **⚡ Vector Search**: Uses FAISS vector database for fast and accurate document retrieval
- **🏷️ Smart Metadata**: Automatically tags documents by policy type for better organization

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Ollama** - Install from [ollama.ai](https://ollama.ai)
   - After installation, pull the required models:
   ```bash
   ollama pull nomic-embed-text
   ollama pull gemma3:1b
   ```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/DocGenius.git
   cd DocGenius
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Ollama is running**
   ```bash
   # Start Ollama service if not already running
   ollama serve
   ```

---

## 📖 Usage

### Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **The app will automatically open in your browser** (typically at http://localhost:8501)

### Using DocGenius

1. **Upload Documents**
   - Click on the sidebar and upload PDF or DOCX files
   - Supports multiple file uploads

2. **Build Vector Database**
   - Click "🔨 Build Vector Database" button
   - Wait for processing to complete (may take a few minutes depending on document size)
   - Refresh the page after completion

3. **Start Chatting**
   - Type your question in the chat input at the bottom
   - The AI will analyze your documents and provide answers with source citations
   - Click "📚 View Sources" to see the exact document sections used

4. **Manage Your Database**
   - **Clear Chat**: Remove conversation history
   - **Delete DB**: Remove the vector database and start fresh

---

## 🛠️ Configuration

### Using Different AI Models

You can customize the models used by setting environment variables:

```bash
# Set embedding model (default: nomic-embed-text)
export EMBEDDING_MODEL="nomic-embed-text"

# Set chat model (default: gemma3:1b)
export CHAT_MODEL="gemma3:1b"
```

Or modify the defaults in `first.py`:

```python
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gemma3:1b")
```

### Available Ollama Models

- **Chat Models**: `gemma3:1b`, `llama2`, `mistral`, `phi3`, etc.
- **Embedding Models**: `nomic-embed-text`, `all-minilm`, `mxbai-embed-large`, etc.

Install additional models:
```bash
ollama pull model-name
```

---

## 📁 Project Structure

```
DocGenius/
├── app.py                      # Main Streamlit application
├── first.py                    # Vector database builder and RAG pipeline
├── create_pdf.py              # PDF creation utility
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── SOURCE_CITATIONS.md        # Source attribution information
├── files/                     # Directory for uploaded documents
└── vectordb/                  # FAISS vector database storage
    ├── index.faiss           # Vector index
    └── index.pkl             # Metadata
```

---

## 🔧 Technical Details

### Tech Stack

- **Frontend**: Streamlit
- **LLM Framework**: LangChain 0.2.x
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: Ollama (nomic-embed-text)
- **LLM**: Ollama (gemma3:1b)
- **Document Loaders**: 
  - PyMuPDF (for PDFs with better image handling)
  - Docx2txt (for Word documents)

### How It Works

1. **Document Processing**:
   - Documents are loaded and split into chunks (1000 characters with 200 character overlap)
   - Each chunk is converted into vector embeddings using the Ollama embedding model
   - Embeddings are stored in a FAISS vector database for fast retrieval

2. **Question Answering**:
   - User question is converted to an embedding
   - Similar document chunks are retrieved from the vector database (top 5 by default)
   - Retrieved context + question are sent to the LLM
   - LLM generates a detailed answer based on the context

3. **Source Attribution**:
   - Original source documents and page numbers are preserved in metadata
   - Sources are displayed with each answer for verification

---

## 🎯 Use Cases

- **Document Analysis**: Quickly find information in large document collections
- **Policy Documents**: Search through company policies, procedures, and guidelines
- **Research Papers**: Extract information from academic papers and reports
- **Legal Documents**: Query contracts, agreements, and legal documents
- **Educational**: Study materials, textbooks, and course notes
- **Business**: Process manuals, technical documentation, and specifications

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: "No vector database found!"
- **Solution**: Upload documents and click "Build Vector Database" button

**Issue**: "Error loading RAG pipeline"
- **Solution**: Ensure Ollama is running (`ollama serve`) and required models are installed

**Issue**: "Failed to load PDF"
- **Solution**: Ensure PDF has readable text content (not just images). For scanned PDFs, use OCR first.

**Issue**: Connection errors to Ollama
- **Solution**: Check if Ollama is running on port 11434 (default)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) - Framework for building LLM applications
- [Ollama](https://ollama.ai) - Local LLM runtime
- [Streamlit](https://streamlit.io) - Web application framework
- [FAISS](https://github.com/facebookresearch/faiss) - Vector similarity search library

---

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

## 🔐 Privacy & Security

DocGenius is designed with privacy in mind:
- ✅ **No external API calls** - Everything runs locally
- ✅ **No data collection** - Your documents never leave your machine
- ✅ **No tracking** - No analytics or telemetry
- ✅ **Open source** - Fully transparent and auditable code

---

<div align="center">

**Made with ❤️ by your friendly AI assistant**

⭐ Star this repository if you find it helpful!

</div>
