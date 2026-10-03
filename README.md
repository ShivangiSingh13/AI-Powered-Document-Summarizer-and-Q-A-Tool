# 🤖 AI-Powered Document Summarizer & Q&A Tool

An AI-powered web application that lets you upload a PDF or DOCX document, get an automatic summary, and ask natural-language questions about its contents — powered by **OpenAI GPT-4** and built with **Streamlit**.

![Tech](https://img.shields.io/badge/Tech-Python%20%7C%20Streamlit-blue)
![AI](https://img.shields.io/badge/AI-OpenAI%20GPT--4-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Usage](#-usage)
- [Deployment](#-deployment)
- [Future Improvements](#-future-improvements)
- [License](#-license)

---

## 🚀 Overview

Reading through long reports, research papers, or contracts just to find a few key facts is slow. This tool lets you upload a document and immediately get:
- A concise, readable summary
- The ability to ask specific questions about the document in plain English, with GPT-4 answering based on the document's actual content

It's designed to be simple to run locally or deploy, with no database required — documents are processed on the fly.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📤 Document Upload | Upload `.pdf` or `.docx` files directly through the web interface |
| ✨ Smart Summarizer | Extracts a concise, readable summary from long documents |
| 💬 Q&A Chat | Ask natural-language questions like *"What is the main topic?"* or *"What are the key points?"* |
| 🧠 GPT-4 Powered | Uses the OpenAI GPT-4 API for both summarization and question-answering |
| 📥 Export Summary | Download the generated summary as a file for later use |
| ☁️ Deploy Anywhere | Easy to deploy via Streamlit Cloud or Hugging Face Spaces |

---

## 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Core language |
| Streamlit | Web UI framework |
| OpenAI GPT-4 API | Summarization and question-answering |
| PyPDF2 / pdfplumber | PDF text extraction |
| docx2txt | DOCX text extraction |
| python-dotenv | Secure API key management via `.env` |
| FPDF | Exporting results to PDF (optional) |

---

## 📂 Project Structure

```
AI-Powered-Document-Summarizer-and-Q-A-Tool/
│
├── app.py                  # Main Streamlit application entry point
├── embedding.py             # Document embedding / text processing logic
├── utils.py                 # Helper functions (text extraction, formatting, etc.)
├── sample_docs/              # Example documents for testing
├── uploaded/                  # Runtime storage for user-uploaded documents
├── outputs/                   # Generated summaries / exported files
├── requirements.txt           # Python dependencies
├── runtime.txt                # Python runtime version (for deployment platforms)
├── DejaVuSans*.ttf / *.pkl    # Fonts used for PDF export via FPDF
└── README.md
```

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.x
- An OpenAI API key

### Installation

```bash
git clone https://github.com/ShivangiSingh13/AI-Powered-Document-Summarizer-and-Q-A-Tool.git
cd AI-Powered-Document-Summarizer-and-Q-A-Tool
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

The app uses `python-dotenv` to load this key securely at runtime — never commit your actual `.env` file to GitHub.

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Then in the browser window that opens:
1. Upload a `.pdf` or `.docx` file
2. Wait for the summary to generate
3. Use the chat/question box to ask anything about the document
4. Download the summary if needed

---

## ☁️ Deployment

This project is set up to deploy easily on:
- **Streamlit Community Cloud** — connect your GitHub repo directly, set `OPENAI_API_KEY` as a secret in the app settings
- **Hugging Face Spaces** — use the Streamlit SDK option, add `OPENAI_API_KEY` as a Space secret

The included `runtime.txt` specifies the Python version for platforms that read it during deployment.

---

## 📌 Future Improvements

- Support for more file types (`.txt`, `.pptx`, scanned/OCR'd PDFs)
- Multi-document Q&A (ask questions across several uploaded files at once)
- Chat history per document session
- Swap in a cheaper/open-source model option alongside GPT-4 for cost flexibility
- Add source-highlighting so answers reference the exact part of the document they came from

---

## 📄 License

This project is developed for learning and portfolio demonstration purposes.
