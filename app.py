# app.py
import streamlit as st
from pdfreader import extract_text_from_pdf
from aimodel import (
    summarize_text,
    extract_important_points,
    answer_question_from_document
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="📄 SmartStudy AI",
    page_icon="",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* Global font & background */
html, body, [class*="css"] {
    font-family: 'Times New Roman', serif;
    background: linear-gradient(120deg, #bbf7d0, #f0fff4);
}

/* Headers & text */
h2, h3, h4, p, div, span {
    font-family: 'Times New Roman', serif;
    color: #064e3b;
}

/* Buttons */
div.stButton > button {
    background-color: #10b981;
    color: white;
    font-weight: bold;
    border-radius: 12px;
    padding: 10px 20px;
    font-family: 'Times New Roman', serif;
    transition: 0.3s;
}
div.stButton > button:hover {
    background-color: #047857;
    transform: scale(1.05);
}

/* Card style with fade-in animation */
.card {
    background-color: #dcfce7;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
    opacity: 0;
    animation: fadeIn 0.8s forwards;
}

/* Drag & drop box with bounce animation */
.drag-drop-box {
    border: 3px dashed #10b981;
    border-radius: 12px;
    padding: 40px;
    text-align: center;
    color: #065f46;
    background-color: #dcfce7;
    font-family: 'Times New Roman', serif;
    transition: 0.3s;
    margin-bottom: 20px;
}
.drag-drop-box:hover {
    background-color: #bbf7d0;
    border-color: #047857;
    transform: scale(1.02);
}
.drag-drop-box p { font-size: 18px; margin: 0; font-weight: bold; }

/* Input field */
input[type=text] {
    border-radius: 8px;
    padding: 8px;
    border: 1px solid #10b981;
    font-family: 'Times New Roman', serif;
}

/* Fade-in animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    "<h2 style='font-family: \"Times New Roman\", serif;'>🤖 SmartStudy with AI</h2>", 
    unsafe_allow_html=True
)
st.markdown(
    "<p style='font-family: \"Times New Roman\", serif;'>Understand documents faster with AI-powered summary, key points, and Q&A</p>", 
    unsafe_allow_html=True
)
st.markdown("---")

# ---------------- PDF UPLOAD ----------------
st.markdown("<p style='font-family: \"Times New Roman\", serif;'> 📄 Upload Document</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(label="", type="pdf", key="pdf_upload")

if uploaded_file:
    st.markdown(f"<div class='drag-drop-box'>✅ PDF uploaded: {uploaded_file.name}</div>", unsafe_allow_html=True)
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("PDF uploaded successfully ✅")
else:
    st.markdown("<div class='drag-drop-box'><p>Drag & Drop a PDF here or click to upload</p></div>", unsafe_allow_html=True)


# ---------------- TABS FOR FUNCTIONALITY ----------------
if uploaded_file:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Summary", "📌 Key Points", "❓ Q&A", "🔎 Search PDF", "🔊 Audio / Export"])

    # ---------- SUMMARY TAB ----------
    with tab1:
        st.markdown("<p>Get a clear and concise overview of the document</p>", unsafe_allow_html=True)
        if st.button("✨ Generate Summary", key="summary_btn"):
            placeholder = st.empty()
            with st.spinner("Generating summary..."):
                summary = summarize_text(pdf_text)
            placeholder.markdown(f"<div class='card'>{summary}</div>", unsafe_allow_html=True)

    # ---------- KEY POINTS TAB ----------
    with tab2:
        st.markdown("<p>Extract the key ideas in simple bullet points</p>", unsafe_allow_html=True)
        if st.button("✨ Extract Important Points", key="points_btn"):
            placeholder = st.empty()
            with st.spinner("Extracting key points..."):
                points = extract_important_points(pdf_text)
            placeholder.markdown(f"<div class='card'>{points}</div>", unsafe_allow_html=True)

    # ---------- Q&A TAB ----------
    with tab3:
        st.markdown("<p>Ask questions and get answers directly from the document</p>", unsafe_allow_html=True)
        user_question = st.text_input("Type your question here")
        if st.button("🔍 Get Answer", key="qa_btn"):
            if user_question.strip() == "":
                st.warning("Please enter a question")
            else:
                placeholder = st.empty()
                with st.spinner("Finding answer..."):
                    answer = answer_question_from_document(pdf_text, user_question)
                placeholder.markdown(f"<div class='card'>{answer}</div>", unsafe_allow_html=True)

    # ---------- SEARCH TAB ----------
    with tab4:
        st.markdown("<p>Search for keywords or phrases in the PDF</p>", unsafe_allow_html=True)
        query = st.text_input("Enter keyword to search", key="search_input")
        if st.button("🔎 Search", key="search_btn"):
            if query.strip() == "":
                st.warning("Please enter a search term")
            else:
                from features.search import search_in_pdf
                results = search_in_pdf(pdf_text, query)
                for r in results:
                    st.markdown(f"<div class='card'>{r}</div>", unsafe_allow_html=True)

    # ---------- AUDIO / EXPORT TAB ----------
    with tab5:
        st.markdown("<p>Listen to summary or export it as PDF</p>", unsafe_allow_html=True)
        # Ensure summary is already generated
        if 'summary' in locals():
            if st.button("🔊 Play Summary Audio", key="audio_btn"):
                from features.tts import text_to_speech
                audio_file = text_to_speech(summary)
                st.audio(audio_file)
            if st.button("📄 Export Summary as PDF", key="export_btn"):
                from features.export import export_to_pdf
                pdf_file = export_to_pdf("Document Summary", summary)
                st.success(f"Summary exported: {pdf_file}")
        else:
            st.info("Generate the summary first in the Summary tab.")
