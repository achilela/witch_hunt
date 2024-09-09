import streamlit as st
from fpso_layout import draw_fpso_layout
from llama_setup import setup_llama_index, create_react_agent
from chat_interface import render_chat_interface
from streamlit_config import set_page_config, apply_custom_css
from utils import load_environment_variables

def main():
    # Load environment variables
    load_environment_variables()
    set_page_config()
    apply_custom_css()

    st.sidebar.title('FPSO Units')

    # Initialize or update OCTOAI_API_KEY in session state
    if 'OCTOAI_API_KEY' not in st.session_state:
        st.session_state.OCTOAI_API_KEY = st.sidebar.text_input("Enter your OCTOAI API key:", type="password")
    else:
        # If already set, display but don't allow editing for simplicity
        st.sidebar.text_input("Your OCTOAI API key:", st.session_state.OCTOAI_API_KEY, disabled=True)

    if st.session_state.OCTOAI_API_KEY:
        setup_llama_index(st.session_state.OCTOAI_API_KEY)
        
        # Initialize or update selected_unit in session state
        if 'selected_unit' not in st.session_state:
            st.session_state.selected = st.sidebar.selectbox('Select FPSO Unit', ['CLV', 'PAZ', 'DAL', 'GIR'])
        else:
            # If already set, maintain the selection
            st.session_state.selected_unit = st.sidebar.selectbox('Select FPSO Unit', ['CLV', 'PAZ', 'DAL', 'GIR'], index=['CLV', 'PAZ', 'DAL', 'GIR'].index(st.session_state.selected_unit))

        if st.sidebar.button('Let me handle your SAP Data'):
            st.sidebar.success('SAP data pre-processing started. This may take a few moments.')
            # Placeholder for SAP data processing
            st.sidebar.success('SAP data pre-processing completed!')

        uploaded_files = st.sidebar.file_uploader("Upload PDF Documents", type=['pdf'], accept_multiple_files=True)

        agent = create_react_agent(uploaded_files)

        render_chat_interface(agent)
        
        st.markdown("### FPSO Visualization")
        draw_fpso_layout(st.session_state.selected_unit)
    else:
        st.warning("Please enter your OCTOAI API key in the sidebar to use the app.")

if __name__ == "__main__":
    main()
