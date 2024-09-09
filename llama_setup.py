import streamlit as st
import os
import tempfile
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
#from llama_index import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.embeddings import OctoAIEmbedding
from llama_index.core import Settings
from llama_index.core.agent import ReActAgent
from llama_index.core.llms import OpenAILike

def setup_llama_index(OCTOAI_API_KEY):
    Settings.embed_model = OctoAIEmbedding(api_key=OCTOAI_API_KEY)

    llm = OpenAILike(
        model="meta-llama-3.1-70b-instruct",
        api_base="https://text.octoai.run/v1",
        api_key=OCTOAI_API_KEY,
        context_window=40000,
        is_function_calling_model=True,
        is_chat_model=True,
    )

    st.session_state.llm = llm
    return llm

def create_react_agent(uploaded_files):
    if 'storage_context' not in st.session_state:
        st.session_state.storage_context = StorageContext.from_defaults()

    if 'llm' not in st.session_state:
        st.error("LLM not initialized. Please enter your OCTOAI API key first.")
        return None

    try:
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)
        index_loaded = True
    except:
        index_loaded = False

    if uploaded_files and not index_loaded:
        all_docs = []
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file_path = temp_file.name

            docs = SimpleDirectoryReader(input_files=[temp_file_path]).load_data()
            all_docs.extend(docs)

            os.unlink(temp_file_path)

        index = VectorStoreIndex.from_documents(all_docs, storage_context=st.session_state.storage_context, show_progress=False)

        st.session_state.storage_context.persist(persist_dir="./storage")
        st.sidebar.success(f"{len(uploaded_files)} document(s) processed and indexed.")

        index_loaded = True

    if index_loaded:
        query_engine = index.as_query_engine(similarity_top_k=3, llm=st.session_state.llm)

        query_engine_tool = QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name="document_index",
                description="Provides information from the uploaded documents. Use a detailed plain text question as input to the tool."
            )
        )

        return ReActAgent.from_tools([query_engine_tool], llm=st.session_state.llm, verbose=True, max_turns=10)

    return None
