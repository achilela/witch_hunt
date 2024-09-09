import streamlit as st
import os
from dotenv import load_dotenv
from fpso_layout import draw_fpso_layout
from llama_setup import setup_llama_index, create_react_agent
from chat_interface import render_chat_interface
from streamlit_config import set_page_config, apply_custom_css
from utils import load_environment_variables

# Load environment variables
load_dotenv()
load_environment_variables()

def main():
    set_page_config()
    apply_custom_css()

    st.sidebar.title('FPSO Units')

    # Fetch API key from environment or prompt user if not set
    OCTOAI_API_KEY = os.getenv('OCTOAI_API_KEY')
    if not OCTOAI_API_KEY:
        st.sidebar.warning("API Key not found in environment. Please set OCTOAI_API_KEY in your environment variables.")
        st.stop()

    # Store API key in session state for future use (for demonstration, typically you'd use environment variables)
    if 'OCTOAI_API_KEY' not in st.session_state:
        st.session_state.OCTOAI_API_KEY = OCTOAI_API_KEY

    # Setup with API key
    setup_llama_index(st.session_state.OCTOAI_API_KEY)

    # User interface elements
    selected_unit = st.selectbox('Select FPSO Unit', ['CLV', 'PAZ', 'DAL', 'GIR'])

    if st.sidebar.button('Let me handle your SAP Data'):
        st.sidebar.success('SAP data pre-processing started. This may take a few moments.')
        # Placeholder for SAP data processing
        st.sidebar.success('SAP data pre-processing completed!')

    uploaded_files = st.sidebar.file_uploader("Upload PDF Documents", type=['pdf'], accept_multiple_files=True)

    # Create agent with uploaded files
    agent = create_react_agent(uploaded_files)

    # Render chat interface
    render_chat_interface(agent)
    
    st.markdown("### FPSO Visualization")
    draw_fpso_layout(selected_unit)

if __name__ == "__main__":
    main()
