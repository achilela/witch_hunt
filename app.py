from llama_setup import setup_llama_index, create_react_agent
from chat_interface import render_chat_interface
from streamlit_config import set_page_config, apply_custom_css
from utils import load_environment_variables
# Directly set the OCTOAI_API_KEY here. Remember to remove this or secure it before sharing or deploying the code.
#OCTOAI_API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNkMjMzOTQ5In0.eyJzdWIiOiJjOTY4MTlhOS05MDRiLTQ2MGItYWVhZS00MDVlMTI1OTAzM2EiLCJ0eXBlIjoidXNlckFjY2Vzc1Rva2VuIiwidGVuYW50SWQiOiI3NTNmNGY4ZC0yNGFmLTRiYTctOTVjMi0wODY1MjJhMDE5OWMiLCJ1c2VySWQiOiIxZGYyY2ZmZC0yYzliLTQ2YTYtOWFlOS0yMzJkZDdhZWY5M2YiLCJhcHBsaWNhdGlvbklkIjoiYTkyNmZlYmQtMjFlYS00ODdiLTg1ZjUtMzQ5NDA5N2VjODMzIiwicm9sZXMiOlsiRkVUQ0gtUk9MRVMtQlktQVBJIl0sInBlcm1pc3Npb25zIjpbIkZFVENILVBFUk1JU1NJT05TLUJZLUFQSSJdLCJhdWQiOiIzZDIzMzk0OS1hMmZiLTRhYjAtYjdlYy00NmY2MjU1YzUxMGUiLCJpc3MiOiJodHRwczovL2lkZW50aXR5Lm9jdG8uYWkiLCJpYXQiOjE3MjY4MTA2NzZ9.Axmgb07O2a4HtsmwgZ_7Wl_rvsvRQggWzuHviulx8kR1EWJ_aZ8CBiYeW2yRrjTlax36LeIIFDY73j_5vb87RWBsBtpAyLMheV7CLoiPQZUeQQLpFlNBMYS-9bn55gjxQCPGsopE2ZtEfSk33f__t-zh3j6Cyq-K2Ukj9wrvDh664iXE2nbpN27HEyKkcId-utgaoxOS2dV1oBsNslWkkcVotmgH-oEk_p41S89FAQNnmXJfY-c2Dat82WiGEfaHFIn_0_wb2vrcEQxdIDtlqFpBnBQAVAmi2qIQgeB9Bn0cjV8qGlN0_HUmGlqrdxnaWjF03ZGcrpLI4nLT1Da4CQ"

def main():
    load_environment_variables()
    set_page_config()
    apply_custom_css()

    st.sidebar.title('FPSO Units')
    
    OCTOAI_API_KEY = st.sidebar.text_input("Enter your OCTOAI API key:", type="password")

    if OCTOAI_API_KEY:
        setup_llama_index(OCTOAI_API_KEY)
        
        selected_unit = st.sidebar.selectbox('Select FPSO Unit', ['CLV', 'PAZ', 'DAL', 'GIR'])
    setup_llama_index(OCTOAI_API_KEY)
    
    selected_unit = st.sidebar.selectbox('Select FPSO Unit', ['CLV', 'PAZ', 'DAL', 'GIR'])

        if st.sidebar.button('Let me handle your SAP Data'):
            st.sidebar.success('SAP data pre-processing started. This may take a few moments.')
            # Placeholder for SAP data processing
            st.sidebar.success('SAP data pre-processing completed!')
    if st.sidebar.button('Let me handle your SAP Data'):
        st.sidebar.success('SAP data pre-processing started. This may take a few moments.')
        # Placeholder for SAP data processing
        st.sidebar.success('SAP data pre-processing completed!')

        uploaded_files = st.sidebar.file_uploader("Upload PDF Documents", type=['pdf'], accept_multiple_files=True)
    uploaded_files = st.sidebar.file_uploader("Upload PDF Documents", type=['pdf'], accept_multiple_files=True)

        agent = create_react_agent(uploaded_files)
    agent = create_react_agent(uploaded_files)

        render_chat_interface(agent)
        
        st.markdown("### FPSO Visualization")
        draw_fpso_layout(selected_unit)
    else:
        st.warning("Please enter your OCTOAI API key in the sidebar to use the app.")
   _chat_interface(agent)
    
    st.markdown("### FPSO Visualization")
    draw_fpso_layout(selected_unit)

if __name__ == "__main__":
    main()
