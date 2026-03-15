import streamlit as st
from transformers import pipeline
from my_socx_script import extract_text_from_pdf, extract_text_from_docx
from io import BytesIO
from fpdf import FPDF
from datetime import datetime
import textwrap
import os

# Load transformers pipelines
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Session states
if "file_history" not in st.session_state:
    st.session_state.file_history = []

if "summaries" not in st.session_state:
    st.session_state.summaries = {}

if "file_texts" not in st.session_state:
    st.session_state.file_texts = {}

# App UI
st.set_page_config(page_title="Doc Summarizer & QA", layout="centered")
st.title("📄 Doc Summarizer & QA")
st.markdown("Upload PDF or DOCX files. Summarize content, ask questions, and export results.")

uploaded_files = st.file_uploader("Upload PDF or DOCX files", type=["pdf", "docx"], accept_multiple_files=True)

# Helper to split large text
def split_text(text, max_chunk_size=1024):
    paragraphs = text.split('\n')
    chunks, current_chunk = [], ""
    for para in paragraphs:
        if len(current_chunk) + len(para) < max_chunk_size:
            current_chunk += para + '\n'
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + '\n'
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks

# File handling
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_type = file_name.split('.')[-1].lower()
        bytes_data = uploaded_file.read()

        if file_name not in st.session_state.file_history:
            st.session_state.file_history.append(file_name)

        try:
            if file_type == "pdf":
                text = extract_text_from_pdf(BytesIO(bytes_data))
            elif file_type == "docx":
                text = extract_text_from_docx(BytesIO(bytes_data))
            else:
                st.warning(f"❌ Unsupported file format: {file_type}")
                continue
        except Exception as e:
            st.error(f"❌ Error reading file {file_name}: {e}")
            continue

        st.session_state.file_texts[file_name] = text

        with st.expander(f"📘 {file_name} - Extracted Text"):
            st.text_area("Preview", text[:3000], height=250)

        # Summarization
        if st.button(f"📝 Summarize {file_name}"):
            with st.spinner("Summarizing..."):
                try:
                    chunks = split_text(text)
                    summary_chunks = []
                    for chunk in chunks:
                        result = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
                        summary_chunks.append(result[0]['summary_text'])
                    full_summary = "\n\n".join(summary_chunks)
                    st.success("✅ Summary:")
                    st.write(full_summary)
                    st.session_state.summaries[file_name] = full_summary
                except Exception as e:
                    st.error(f"Summarization failed: {e}")

        # QA Section
        st.markdown("#### 🤖 Ask a Question")
        user_question = st.text_input(f"Your question for {file_name}:", key=f"question_{file_name}")
        if user_question:
            with st.spinner("Searching for the answer..."):
                try:
                    answer = qa_pipeline(question=user_question, context=text)
                    st.success(f"**Answer:** {answer['answer']}")
                except Exception as e:
                    st.error(f"QA failed: {e}")

# Sidebar History
if st.session_state.file_history:
    st.sidebar.subheader("📂 File History")
    for file in st.session_state.file_history:
        st.sidebar.write(f"• {file}")

# Export summaries to PDF
if st.session_state.summaries:
    if st.button("📥 Export All Summaries to PDF"):
        try:
            pdf = FPDF()
            pdf.add_page()

            # Load fonts
            font_dir = os.path.dirname(__file__)
            pdf.add_font("DejaVu", "", os.path.join(font_dir, "DejaVuSans.ttf"), uni=True)
            pdf.add_font("DejaVu", "B", os.path.join(font_dir, "DejaVuSans-Bold.ttf"), uni=True)
            pdf.add_font("DejaVu", "I", os.path.join(font_dir, "DejaVuSans-Oblique.ttf"), uni=True)
            pdf.add_font("DejaVu", "BI", os.path.join(font_dir, "DejaVuSans-BoldOblique.ttf"), uni=True)

            pdf.set_font("DejaVu", size=12)
            pdf.set_auto_page_break(auto=True, margin=15)

            pdf.set_font("DejaVu", "B", size=14)
            pdf.cell(200, 10, txt="Document Summaries", ln=True, align='C')
            pdf.ln(10)

            for filename, summary in st.session_state.summaries.items():
                pdf.set_font("DejaVu", "B", size=12)
                pdf.cell(200, 10, txt=filename, ln=True)
                pdf.set_font("DejaVu", "", size=11)
                wrapped_summary = textwrap.wrap(summary, width=100)
                for line in wrapped_summary:
                    pdf.multi_cell(0, 10, line)
                pdf.ln(5)

            # Prepare in-memory download
            export_filename = f"summaries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf_output = BytesIO()
            pdf_bytes = pdf.output(dest='S').encode('latin-1')  # Fix encoding
            pdf_output.write(pdf_bytes)
            pdf_output.seek(0)

            st.download_button(
                label="📄 Download PDF",
                data=pdf_output,
                file_name=export_filename,
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Failed to export PDF: {e}")
