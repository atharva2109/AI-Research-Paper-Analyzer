# AI Research Paper Assistant

An intelligent, fully automated AI assistant that helps you understand
research papers in seconds. Upload any PDF research paper and instantly
get:

✅ **Clean section detection and extraction**\
✅ **Detailed summaries of each section**\
✅ **A chat interface to ask questions grounded in the paper's text**\
✅ **Accurate, citation-aware answers using retrieval-augmented
generation (RAG)**

---

## 🚀 Features

### **1. Upload & Extract**

- Upload any PDF research paper.
- Extracts full text and detects major sections & subsections using
  heuristic parsing + LLM refinement.
- Automatically removes irrelevant items like figures, tables, or
  noise.

### **2. Smart Sectioning**

- Sections are cleaned and normalized via an LLM using
  `refine_section()`.
- Each section is paired with the exact text range using
  `split_sections_with_content()`.
- Enables topic-wise exploration of the paper.

### **3. AI-Generated Summaries**

- Choose any detected section.
- Generates a clear, structured, expert-level summary using Groq LLM.
- Includes simplified explanations for beginners.

### **4. Chat With the Paper**

- Ask questions directly about the research.
- Uses FAISS vector search + embeddings to retrieve exact text chunks.
- Responses come from the actual paper, not hallucinations.

---

## 🧠 System Overview

    PDF → Text Extraction → Section Detection → Section Refinement →
    Topic-wise Text Split → Vector Database (FAISS) → RAG Chat → Answers

---

## 📦 Project Structure

    .
    ├── app.py                         # Flask app entry point
    ├── src/
    │   ├── create_vector_db.py        # Creates FAISS vector DB
    │   ├── detect_and_split_sections.py # Section cleaning + text splitting
    │   ├── generate_summary.py        # Summary generation logic
    │   ├── load_and_extract_text.py   # PDF text extraction utilities
    ├── templates/
    │   └── index.html                 # Frontend UI
    └── uploads/                       # Stored user PDFs

---

## 🔧 Installation & Setup

### **1. Clone the repository**

```bash
git clone <repo-url>
cd <project-folder>
```

### **2. Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

### **4. Add environment variables**

Create a `.env` file:

```env
GROQ_API_KEY=your_key_here
EMBEDDING_MODEL=your_hf_model
LLM_MODEL=your_groq_model
```

### **5. Run the app**

```bash
python app.py
```

Open in browser:

    http://127.0.0.1:5000

---

## 🖥️ Example Workflow

1.  Upload paper → App extracts text.\
2.  Choose a section → AI generates summary.\
3.  Ask any question → RAG ensures grounded answers.

---

## ✅ Future Enhancements

- Multi-paper comparison\
- Reference detection & citation mapping\
- PDF highlighting\
- Exportable summaries\
- Multilingual support

---

## 📜 License

MIT License (or specify your preferred license).
