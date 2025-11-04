# python.py

import streamlit as st
from docx import Document
from io import BytesIO

# -----------------------
# Cấu hình trang
# -----------------------
st.set_page_config(
    page_title="Sổ tay hướng dẫn kiểm tra Agribank Hà Thành",
    page_icon="📘",
    layout="wide"
)

# -----------------------
# CSS tùy chỉnh màu sắc Agribank
# -----------------------
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
        color: #222;
        font-family: 'Segoe UI', sans-serif;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    h1, h2, h3, h4 {
        color: #800000 !important;
    }
    .sidebar .sidebar-content {
        background-color: #8B0000;
        color: white;
    }
    .sidebar .sidebar-content input, .sidebar .sidebar-content select {
        color: black !important;
    }
    .css-1v0mbdj, .stTextInput label, .stSelectbox label {
        color: white !important;
    }
    .stButton button {
        background-color: #800000;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton button:hover {
        background-color: #a00000;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# Logo + tiêu đề
# -----------------------
col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.image("logo_agribank.png", use_column_width=True)
with col2:
    st.title("📘 SỔ TAY HƯỚNG DẪN KIỂM TRA NGHIỆP VỤ")
    st.subheader("Agribank Chi nhánh Hà Thành – Phiên bản số hóa")
st.markdown("---")

# -----------------------
# Hàm đọc file Word
# -----------------------
def load_docx(file_path):
    doc = Document(file_path)
    chapters = {}
    current_chapter = "Khác"

    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue

        if text.lower().startswith("chương"):
            current_chapter = text
            chapters[current_chapter] = []
        else:
            chapters.setdefault(current_chapter, []).append(text)
    return chapters

chapters = load_docx("So_tay_Agribank.docx.docx")

# -----------------------
# Sidebar
# -----------------------
st.sidebar.image("logo_agribank.png", use_column_width=True)
st.sidebar.markdown("### 📑 **Danh mục chương**")

chapter_list = list(chapters.keys())
selected_chapter = st.sidebar.selectbox("Chọn chương:", chapter_list)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💬 **Chatbot hướng dẫn kiểm tra**")

query = st.sidebar.text_input("Nhập từ khóa hoặc câu hỏi (VD: tín dụng, kế toán...)")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 **Tải tài liệu gốc**")

with open("So_tay_Agribank.docx.docx", "rb") as f:
    st.sidebar.download_button(
        label="⬇️ Tải Sổ tay gốc (.docx)",
        data=f,
        file_name="So_tay_Agribank.docx.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

st.sidebar.markdown("---")
st.sidebar.markdown("### ✍️ **Góp ý nội dung**")
feedback = st.sidebar.text_area("Nhập góp ý (nếu có)")
if st.sidebar.button("Gửi góp ý"):
    st.sidebar.success("✅ Cảm ơn bạn! Góp ý đã được ghi nhận.")

# -----------------------
# Nội dung chính
# -----------------------
st.header(f"📂 {selected_chapter}")
for para in chapters[selected_chapter]:
    st.markdown(f"- {para}")

# -----------------------
# Chatbot kết quả (tìm kiếm nâng cao)
# -----------------------
import re
import unicodedata

def normalize_text(text):
    """Chuẩn hóa văn bản: bỏ dấu, chuyển về chữ thường"""
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)]).lower()

if query:
    st.markdown("---")
    st.subheader(f"🔎 Kết quả tìm kiếm cho: *{query}*")

    normalized_query = normalize_text(query)
    results_by_chapter = {}

    for ch, paras in chapters.items():
        for p in paras:
            if normalized_query in normalize_text(p):
                results_by_chapter.setdefault(ch, []).append(p)

    if results_by_chapter:
        for ch, paras in results_by_chapter.items():
            with st.expander(f"📁 {ch} ({len(paras)} kết quả)", expanded=True):
                for para in paras:
                    # Làm nổi bật từ khóa
                    highlighted = re.sub(
                        f"({re.escape(query)})",
                        r"**\1**",
                        para,
                        flags=re.IGNORECASE
                    )
                    st.markdown(f"🔹 {highlighted}")
    else:
        st.info("Không tìm thấy nội dung phù hợp. Hãy thử từ khóa khác.")
