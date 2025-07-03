import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    h1 {
        color: red;
        font-size: 48px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>Hello Styled World</h1>", unsafe_allow_html=True)
