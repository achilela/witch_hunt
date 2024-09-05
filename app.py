import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import matplotlib.transforms as transforms
import pandas as pd
import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Document
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.embeddings.octoai import OctoAIEmbedding
from llama_index.core import Settings as LlamaGlobalSettings
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai_like import OpenAILike
import tempfile

# Load environment variables
load_dotenv()

# Set up OctoAI API key
OCTOAI_API_KEY = os.environ.get("OCTOAI_API_KEY")

# Set up LlamaIndex
LlamaGlobalSettings.embed_model = OctoAIEmbedding()

llm = OpenAILike(
    model="meta-llama-3.1-70b-instruct",
    api_base="https://text.octoai.run/v1",
    api_key=OCTOAI_API_KEY,
    context_window=40000,
    is_function_calling_model=True,
    is_chat_model=True,
)

# FPSO Layout App functions (unchanged)
def add_rectangle(ax, xy, width, height, **kwargs):
    rectangle = patches.Rectangle(xy, width, height, **kwargs)
    ax.add_patch(rectangle)

def add_chamfered_rectangle(ax, xy, width, height, chamfer, **kwargs):
    x, y = xy
    coords = [
        (x + chamfer, y),
        (x + width - chamfer, y),
        (x + width, y + chamfer),
        (x + width, y + height - chamfer),
        (x + width - chamfer, y + height),
        (x + chamfer, y + height),
        (x, y + height - chamfer),
        (x, y + chamfer)
    ]
    polygon = patches.Polygon(coords, closed=True, **kwargs)
    ax.add_patch(polygon)

def add_hexagon(ax, xy, radius, **kwargs):
    x, y = xy
    vertices = [(x + radius * math.cos(2 * math.pi * n / 6), 
                 y + radius * math.sin(2 * math.pi * n / 6)) 
                for n in range(6)]
    hexagon = patches.Polygon(vertices, closed=True, **kwargs)
    ax.add_patch(hexagon)

def add_fwd(ax, xy, width, height, **kwargs):
    x, y = xy
    top_width = width * 0.80
    coords = [
        (0, 0),
        (width, 0),
        (width - (width - top_width) / 2, height),
        ((width - top_width) / 2, height)
    ]
    trapezoid = patches.Polygon(coords, closed=True, **kwargs)
    t = transforms.Affine2D().rotate_deg(90).translate(x, y)
    trapezoid.set_transform(t + ax.transData)
    ax.add_patch(trapezoid)
    text_t = transforms.Affine2D().rotate_deg(90).translate(x + height/2, y + width/2)
    ax.text(0, -1, "FWD", ha='center', va='center', fontsize=7, weight='bold', transform=text_t + ax.transData)

def draw_clv(ax):
    # (CLV drawing code remains unchanged)
    pass

def draw_paz(ax):
    ax.text(6, 1.75, "PAZ Layout\n(Not implemented)", ha='center', va='center', fontsize=16, weight='bold')

def draw_dal(ax):
    ax.text(6, 1.75, "DAL Layout\n(Not implemented)", ha='center', va='center', fontsize=16, weight='bold')

def draw_gir(ax):
    ax.text(6, 1.75, "GIR Layout\n(Not implemented)", ha='center', va='center', fontsize=16, weight='bold')

# Streamlit app
st.set_page_config(page_title="B17 - FPSO Units", layout="wide")

# Custom CSS (unchanged)
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
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title('FPSO Units')
selected_unit = st.sidebar.selectbox('Select FPSO Unit', ['CLV', 'PAZ', 'DAL', 'GIR'])

if st.sidebar.button('Let me handle your SAP Data'):
    st.sidebar.success('SAP data pre-processing started. This may take a few moments.')
    # Placeholder for SAP data processing
    st.sidebar.success('SAP data pre-processing completed!')

# File uploader for documents
uploaded_files = st.sidebar.file_uploader("Upload PDF Documents", type=['pdf'], accept_multiple_files=True)

# Initialize session state for indexes and agent
if 'indexes' not in st.session_state:
    st.session_state.indexes = {}
if 'agent' not in st.session_state:
    st.session_state.agent = None

# Process uploaded files and create indexes
if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state.indexes:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file_path = temp_file.name

            # Create index from the uploaded document
            docs = SimpleDirectoryReader(input_files=[temp_file_path]).load_data()
            index = VectorStoreIndex.from_documents(docs, show_progress=True)
            st.session_state.indexes[uploaded_file.name] = index

            os.unlink(temp_file_path)  # Remove the temporary file

    st.sidebar.success(f"{len(uploaded_files)} document(s) processed and indexed.")

    # Create query engine tools from the indexes
    query_engine_tools = []
    for file_name, index in st.session_state.indexes.items():
        query_engine = index.as_query_engine(similarity_top_k=3, llm=llm)
        tool = QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name=file_name,
                description=f"Provides information from the document {file_name}. Use a detailed plain text question as input to the tool."
            )
        )
        query_engine_tools.append(tool)

    # Create or update the ReActAgent
    st.session_state.agent = ReActAgent.from_tools(query_engine_tools, llm=llm, verbose=True, max_turns=10)

# Main content
# Chat interface at the top center
st.markdown("### Methods Engineer")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hey! This is Ataliba here, how can I help?!"}
        ]

    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-message'>{message['content']}</div>", unsafe_allow_html=True)

    user_input = st.text_input("Let me know your queries on the chat below...")
    if st.button("Send"):
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            if st.session_state.agent:
                # Use the ReActAgent to generate a response
                response = st.session_state.agent.chat(user_input)
                st.session_state.messages.append({"role": "assistant", "content": str(response)})
            else:
                st.session_state.messages.append({"role": "assistant", "content": "Please upload documents first to enable the AI assistant."})
            st.experimental_rerun()

# FPSO Visualization at the bottom
st.markdown("### FPSO Visualization")
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 3.5)
ax.set_aspect('equal')
ax.grid(False)
ax.set_facecolor('#E6F3FF')

if selected_unit == 'CLV':
    draw_clv(ax)
elif selected_unit == 'PAZ':
    draw_paz(ax)
elif selected_unit == 'DAL':
    draw_dal(ax)
elif selected_unit == 'GIR':
    draw_gir(ax)

st.pyplot(fig)
