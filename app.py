import streamlit as st
from fpso_layout import draw_fpso_layout
from llama_setup import setup_llama_index, create_react_agent
from chat_interface import render_chat_interface
from streamlit_config import set_page_config, apply_custom_css
from utils import load_environment_variables

def main():
    load_environment_variables()
    set_page_config()
    apply_custom_css()

    st.sidebar.title('FPSO Units')
    
    # Initialize OCTOAI_API_KEY in session state if it doesn't exist
    if "OCTOAI_API_KEY" not in st.session_state:
        st.session_state.OCTOAI_API_KEY = ""

    # Use text_input to get API key and update session state
    new_api_key = st.sidebar.text_input("Enter your OCTOAI API key:", type="password", value=st.session_state.OCTOAI_API_KEY)
    
    # Update session state if a new key is entered
    if new_api_key != st.session_state.OCTOAI_API_KEY:
        st.session_state.OCTOAI_API_KEY = new_api_key
        st.rerun()  # Rerun the app to reflect changes

    if st.session_state.OCTOAI_API_KEY:
        setup_llama_index(st.session_state.OCTOAI_API_KEY)
        
        selected_unit = st.sidebar.selectbox('Select FPSO Unit', ['CLV', 'PAZ', 'DAL', 'GIR'])

        if st.sidebar.button('Let me handle your SAP Data'):
            st.sidebar.success('SAP data pre-processing started. This may take a few moments.')
            # Placeholder for SAP data processing
            st.sidebar.success('SAP data pre-processing completed!')

        uploaded_files = st.sidebar.file_uploader("Upload PDF Documents", type=['pdf'], accept_multiple_files=True)

        agent = create_react_agent(uploaded_files)

        render_chat_interface(agent)
        
        st.markdown("### FPSO Visualization")
        draw_fpso_layout(selected_unit)
    else:
        st.warning("Please enter your OCTOAI API key in the sidebar to use the app.")

if __name__ == "__main__":
    main()
