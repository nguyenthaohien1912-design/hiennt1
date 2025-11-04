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
@st.cache_data
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

chapters = load_docx("so_tay.docx")

# -----------------------
# Sidebar
# -----------------------
st.sidebar.image("agribank_logo.png", use_column_width=True)
st.sidebar.markdown("### 📑 **Danh mục chương**")

chapter_list = list(chapters.keys())
selected_chapter = st.sidebar.selectbox("Chọn chương:", chapter_list)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💬 **Chatbot hướng dẫn kiểm tra**")

query = st.sidebar.text_input("Nhập từ khóa hoặc câu hỏi (VD: tín dụng, kế toán...)")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 **Tải tài liệu gốc**")

with open("so_tay.docx", "rb") as f:
    st.sidebar.download_button(
        label="⬇️ Tải Sổ tay gốc (.docx)",
        data=f,
        file_name="So_tay_huong_dan_kiem_tra_Agribank.docx",
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
# Chatbot kết quả
# -----------------------
if query:
    st.markdown("---")
    st.subheader(f"🔍 Kết quả tìm kiếm cho: *{query}*")

    results = []
    for ch, paras in chapters.items():
        for p in paras:
            if query.lower() in p.lower():
                results.append(f"**[{ch}]** {p}")

    if results:
        for r in results[:8]:
            st.markdown(f"🔹 {r}")
    else:
        st.info("Không tìm thấy nội dung phù hợp. Hãy thử từ khóa khác.")
