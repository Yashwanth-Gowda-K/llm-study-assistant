# AI Study Assistant — RAG

A beginner-friendly AI study assistant that answers questions using information retrieved from study notes and PDF documents.

## 🎯 Goal

Learn how to build an LLM application from scratch, including embeddings, vector databases, retrieval, and answer generation.

## 🚀 Features

- Extract text from PDF documents.
- Split text into smaller chunks.
- Convert text into embeddings using Google's Gemini API.
- Store and retrieve information using ChromaDB.
- Retrieve relevant context for a user's question.
- Generate answers using Gemini.
- Interact with the assistant through a Streamlit interface.

## 🛠️ Technologies

- Python
- Google Gemini API
- ChromaDB
- Streamlit
- FastAPI
- PyPDF
- Git and GitHub

## 📂 Project Structure

```text
llm-study-assistant/
├── app/
│   ├── answer.py
│   ├── chunking.py
│   ├── indexer.py
│   ├── pdf_reader.py
│   ├── retriever.py
│   ├── streamlit_app.py
│   └── main.py
├── data/
├── documents/
├── docs/
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

*Note: This is a simplified overview; some local files and folders are intentionally excluded.*

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/Yashwanth-Gowda-K/llm-study-assistant.git
cd llm-study-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Never commit your real API key to GitHub.

### 5. Add a PDF

Place your study PDF inside the `documents/` folder.

### 6. Index the PDF

Run the indexing script according to the project's current implementation:

```bash
python -m app.indexer
```

### 7. Start the Streamlit interface

```bash
streamlit run app/streamlit_app.py
```

## 🧠 How It Works

1. **Read:** Extract text from a PDF.
2. **Chunk:** Split the text into smaller pieces.
3. **Embed:** Convert the chunks into numerical vectors.
4. **Store:** Save the vectors in ChromaDB.
5. **Retrieve:** Find relevant information for a question.
6. **Generate:** Ask Gemini to produce an answer using the retrieved context.

## 📌 Project Status

The project includes PDF processing, chunking, embedding, retrieval, answer generation, and a Streamlit interface.

Further testing and improvements are still needed.

## 🎓 Learning Objective

Understand how RAG applications work by building each component step by step rather than relying entirely on ready-made frameworks.