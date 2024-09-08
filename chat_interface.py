import streamlit as st
import asyncio

async def stream_response(agent, user_input):
    response = await agent.achat(user_input)
    words = str(response).split()
    full_response = ""
    for word in words:
        full_response += word + " "
        yield full_response
        await asyncio.sleep(0.01)

def render_chat_interface(agent):
    st.markdown("<h3 style='text-align: center; font-size: 20px; font-weight: normal;'>Methods Engineer</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        user_input = st.text_input("This is Ataliba here, I am here to help you...", key="chat_input", max_chars=None)

        if st.button("Send"):
            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                if agent:
                    with st.empty():
                        st.write("Let me think...")
                        
                        async def run_stream():
                            response_placeholder = st.empty()
                            full_response = ""
                            async for chunk in stream_response(agent, user_input):
                                full_response = chunk
                                response_placeholder.markdown(f"<div class='bot-message'>{full_response}</div>", unsafe_allow_html=True)
                            return full_response

                        full_response = asyncio.run(run_stream())
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.session_state.messages.append({"role": "assistant", "content": "Please upload documents first to enable the AI assistant."})
                
                st.rerun()

        chat_container = st.container()
        with chat_container:
            if len(st.session_state.messages) > 1:
                st.markdown(f"<div class='user-message'>{st.session_state.messages[-2]['content']}</div>", unsafe_allow_html=True)
            if len(st.session_state.messages) > 0 and st.session_state.messages[-1]['role'] == 'assistant':
                st.markdown(f"<div class='bot-message'>{st.session_state.messages[-1]['content']}</div>", unsafe_allow_html=True)
