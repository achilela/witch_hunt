import streamlit as st

def set_page_config():
    st.set_page_config(page_title="B17 - FPSO Units", layout="wide")

def apply_custom_css():
    st.markdown("""
    <style>
        .chat-container {
            border: 1px solid #4CAF50;
            border-radius: 5px;
            padding: 10px;
            background-color: #1e1e1e;
            color: #c9d1d9;
            height: 300px;
            overflow-y: auto;
            margin-bottom: 10px;
        }
        .user-message {
            background-color: #2f3136;
            color: #ffffff;
            border-radius: 15px;
            padding: 8px 12px;
            margin: 5px 0;
            max-width: 70%;
            align-self: flex-end;
        }
        .bot-message {
            background-color: #40444b;
            color: #ffffff;
            border-radius: 15px;
            padding: 8px 12px;
            margin: 5px 0;
            max-width: 70%;
            align-self: flex-start;
        }
        .stTextInput input {
            background-color: #262626;
            color: #ffffff;
            border: 1px solid #4CAF50;
            border-radius: 20px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: #ffffff;
            border-radius: 20px;
        }
        .chat-input {
            width: 100% !important;
        }
    </style>
    """, unsafe_allow_html=True)
