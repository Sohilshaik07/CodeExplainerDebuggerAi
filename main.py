import streamlit as st
from process import explain_code, debug_code
import io

st.set_page_config(layout="wide", page_title="Chat Bot: AI For Developers", page_icon="🤖")

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

body {
    background-color: #000000;
    color: #00FF00;
    font-family: 'JetBrains Mono', monospace;
}

.main .block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

h1 {
    color: #00FF00;
    font-size: 2.5rem;
    font-weight: bold;
}

.stTextInput input, .stTextArea textarea, .stSelectbox div, .stFileUploader label {
    background-color: #101010 !important;
    color: #00FF00 !important;
    border: 1px solid #333 !important;
    border-radius: 6px;
}

.stButton > button {
    background-color: #00FF00 !important;
    color: #000000 !important;
    font-weight: bold;
    padding: 0.5rem 1.5rem;
    border-radius: 8px;
}

.stButton > button:hover {
    background-color: #33FF33 !important;
}

.control-title {
    background-color: black;
    color: lime;
    padding: 0.4rem 1rem;
    border-radius: 8px;
    display: inline-block;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.radio-horizontal label {
    display: inline-block !important;
    margin-right: 20px;
}

.chat-bubble-ai {
    background-color: #111;
    color: #C2F5C2;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    border: 1px solid #3C3C3C;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("## 🤖 Chat Bot : AI For Developers")

# Code input section
code_input = st.text_area("Write your code here... 🧑‍💻", height=300)

# Controls section - moved BELOW code input
st.markdown("---")
cols = st.columns([2, 2, 2, 2])

# Upload Section
with cols[0]:
    st.markdown("📂 <span class='control-title'>Upload File</span>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Drag and drop file here", type=["py", "js", "java", "cpp", "html", "txt"])

# Language Section
with cols[1]:
    st.markdown("🌐 <span class='control-title'>Select Language</span>", unsafe_allow_html=True)
    languages = ["Python", "JavaScript", "Java", "C++", "HTML", "Text", "Other"]
    language = st.radio("Choose Language", languages, horizontal=True, key="lang_radio")

    if language == "Other":
        language = st.text_input("Specify the language:")

# Action Section
with cols[2]:
    st.markdown("🛠️ <span class='control-title'>Action</span>", unsafe_allow_html=True)
    action = st.radio("Select", ("Explain Code", "Debug Code"))

# Run Button
with cols[3]:
    st.markdown("🚀 <span class='control-title'>Run</span>", unsafe_allow_html=True)
    button = st.button("▶️ Run Code")

# Processing logic
if button:
    if uploaded_file is not None:
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        code = stringio.read()
    elif code_input.strip():
        code = code_input
    else:
        st.error("⚠️ Please upload or enter code.")
        st.stop()

    if action == "Explain Code":
        response_stream = explain_code(code, language)
    else:
        response_stream = debug_code(code, language)

    response = ""
    message_placeholder = st.empty()
    for chunk in response_stream:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
            message_placeholder.markdown(f"<div class='chat-bubble-ai'>{response}▌</div>", unsafe_allow_html=True)
    message_placeholder.markdown(f"<div class='chat-bubble-ai'>{response}</div>", unsafe_allow_html=True)
