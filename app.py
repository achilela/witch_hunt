import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import matplotlib.transforms as transforms
import pandas as pd
import io
from streamlit.components.v1 import html

# Set custom font
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Tw Cen MT', 'Arial', 'Helvetica']

# Function to draw straight rectangles without chamfer
def add_rectangle(ax, xy, width, height, **kwargs):
    rectangle = patches.Rectangle(xy, width, height, **kwargs)
    ax.add_patch(rectangle)

# Function to draw chamfered rectangles
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

# Function to draw hexagons
def add_hexagon(ax, xy, radius, **kwargs):
    x, y = xy
    vertices = [(x + radius * math.cos(2 * math.pi * n / 6), 
                 y + radius * math.sin(2 * math.pi * n / 6)) 
                for n in range(6)]
    hexagon = patches.Polygon(vertices, closed=True, **kwargs)
    ax.add_patch(hexagon)

# Function to draw FWD module as a rotated trapezoid
def add_fwd(ax, xy, width, height, **kwargs):
    x, y = xy

    # Define the trapezoid shape
    top_width = width * 0.80  # Narrower at the top
    coords = [
        (0, 0),  # Bottom left
        (width, 0),  # Bottom right
        (width - (width - top_width) / 2, height),  # Top right
        ((width - top_width) / 2, height)  # Top left
    ]

    # Create the trapezoid
    trapezoid = patches.Polygon(coords, closed=True, **kwargs)

    # Create a rotation transform
    t = transforms.Affine2D().rotate_deg(90).translate(x, y)
    trapezoid.set_transform(t + ax.transData)

    # Add the rotated trapezoid
    ax.add_patch(trapezoid)

    # Add rotated text
    text_t = transforms.Affine2D().rotate_deg(90).translate(x + height/2, y + width/2)
    ax.text(0, -1, "FWD", ha='center', va='center', fontsize=7, weight='bold', transform=text_t + ax.transData)

# Custom Streamlit theme
st.set_page_config(page_title="FPSO Units Visualization", layout="wide")

# Custom CSS for font and sizing
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tw+Cen+MT:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Tw Cen MT', sans-serif;
        font-size: 14px;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Tw Cen MT', sans-serif;
    }
    .stTitle, .stMarkdown h1 {
        font-size: 24px !important;
    }
    .stMarkdown h2 {
        font-size: 20px !important;
    }
    .stMarkdown h3 {
        font-size: 18px !important;
    }
    .stSelectbox label, .stFileUploader label, .stButton button {
        font-size: 16px !important;
    }
    /* New styles for chat input */
    .chat-input {
        border-radius: 20px;
        border: 1px solid #ccc;
        padding: 10px 15px;
        font-size: 16px;
        width: 100%;
    }
    .chat-container {
        display: flex;
        align-items: center;
    }
    .chat-icon {
        margin-left: 10px;
        color: #4CAF50;
        font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit app layout
st.sidebar.title('FPSO Units')
selected_unit = st.sidebar.selectbox('Select FPSO Unit', ['CLV', 'PAZ', 'DAL', 'GIR'])

# Add button for pre-processing SAP data
if st.sidebar.button('Pre-process SAP Data'):
    st.sidebar.success('SAP data pre-processing started. This may take a few moments.')
    # Here you would add the actual SAP data processing logic
    # For example:
    # process_sap_data()
    st.sidebar.success('SAP data pre-processing completed!')

# Add file uploader
uploaded_file = st.sidebar.file_uploader("Upload Data File", type=['csv', 'xlsx', 'pdf'])
if uploaded_file is not None:
    # Handle different file types
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        st.sidebar.warning("PDF processing is not implemented in this example.")
        # df = process_pdf(uploaded_file)  # You would need to implement this function
    
    st.sidebar.success(f"File {uploaded_file.name} successfully uploaded and processed!")

# Create a figure and axis for the layout
fig, ax = plt.subplots(figsize=(12, 8))

# Set the axis limits and aspect ratio
ax.set_xlim(0, 12)
ax.set_ylim(0, 3.5)
ax.set_aspect('equal')

# Remove grid
ax.grid(False)

# Add ocean background
ax.set_facecolor('#E6F3FF')  # Light blue color for ocean

# Increase line thickness
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['patch.linewidth'] = 2

# Reduce font size for all text in the plot
plt.rcParams['font.size'] = 6

def draw_clv():
    # Define the layout modules and positions
    modules = {
        'M120': (0.75, 2), 'M121': (0.5, 3), 'M122': (0.5, 4), 'M123': (0.5, 5),
        'M124': (0.5, 6), 'M125': (0.5, 7), 'M126': (0.5, 8), 'M110': (1.75, 2),
        'M111': (2, 3), 'M112': (2, 4), 'M113': (2, 5), 'M114': (2, 6),
        'M115': (2, 7), 'M116': (2, 8)
    }
    racks = {
        'P-RACK 141': (1.5, 3), 'P-RACK 142': (1.5, 4), 'P-RACK 143': (1.5, 5),
        'P-RACK 144': (1.5, 6), 'P-RACK 145': (1.5, 7), 'P-RACK 146': (1.5, 8)
    }
    flare = {
        'FL': (0.5, 9) 
    }
    living_quarters = {
        'LQ': (0.5, 1)
    }
    hexagons = {
        'HELIDECK': (2.75, 1)
    }
    fwd = {
        'FWD': (0.5, 9.5)
    }

    # Draw the M modules
    for module, (row, col) in modules.items():
        if module == 'M110':
            height = 1.25
            y_position = row
            text_y = row + 0.5
        elif module == 'M120':
            height = 1.25
            y_position = row - 0.25
            text_y = row + 0.25
        else:
            height = 1
            y_position = row
            text_y = row + 0.5
        
        add_chamfered_rectangle(ax, (col, y_position), 1, height, 0.1, edgecolor='black', facecolor='white')
        ax.text(col + 0.5, text_y, module, ha='center', va='center', fontsize=7, weight='bold')

    # Draw the RACK modules
    for rack, (row, col) in racks.items():
        width = 1
        add_chamfered_rectangle(ax, (col, row), width, 0.5, 0.05, edgecolor='black', facecolor='white')
        ax.text(col + width / 2, row + 0.25, rack, ha='center', va='center', fontsize=7, weight='bold')

    # Draw the flare with chamfer only at the top
    for flare, (row, col) in flare.items():
        add_chamfered_rectangle(ax, (col, row), 0.5, 2.5, 0.1, edgecolor='black', facecolor='white')
        ax.text(col + 0.25, row + 1.25, flare, ha='center', va='center', fontsize=7, weight='bold')

    # Draw the LQ module
    for living_quarter, (row, col) in living_quarters.items():
        add_rectangle(ax, (col, row), 1, 2.5, edgecolor='black', facecolor='white')
        ax.text(col + 0.5, row + 1.25, living_quarter, ha='center', va='center', fontsize=7, rotation=90, weight='bold')

    # Draw the hexagons
    for hexagon, (row, col) in hexagons.items():
        add_hexagon(ax, (col, row), 0.60, edgecolor='black', facecolor='white')
        ax.text(col, row, hexagon, ha='center', va='center', fontsize=7, weight='bold')

    # Draw the FWD module
    for fwd_module, (row, col) in fwd.items():
        add_fwd(ax, (col, row), 2.5, -1, edgecolor='black', facecolor='white')

def draw_paz():
    ax.text(6, 1.75, "PAZ Layout\n(Not implemented)", ha='center', va='center', fontsize=16, weight='bold')

def draw_dal():
    ax.text(6, 1.75, "DAL Layout\n(Not implemented)", ha='center', va='center', fontsize=16, weight='bold')

def draw_gir():
    ax.text(6, 1.75, "GIR Layout\n(Not implemented)", ha='center', va='center', fontsize=16, weight='bold')

# Draw the selected FPSO unit
if selected_unit == 'CLV':
    draw_clv()
elif selected_unit == 'PAZ':
    draw_paz()
elif selected_unit == 'DAL':
    draw_dal()
elif selected_unit == 'GIR':
    draw_gir()

# Display the figure
st.pyplot(fig)

# Chat-like interface for data interaction
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    html("""
    <div class="chat-container">
        <input type="text" class="chat-input" placeholder="Ask anything" id="chat-input">
        <span class="chat-icon">⚪</span>
    </div>
    <script>
    const input = document.getElementById('chat-input');
    input.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            document.dispatchEvent(new CustomEvent('chat-submit', { detail: input.value }));
            input.value = '';
        }
    });
    </script>
    """, height=70)

    user_input = st.empty()

# JavaScript to handle the custom event
st.components.v1.html(
    """
    <script>
    document.addEventListener('chat-submit', function(e) {
        const data = e.detail;
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: data}, '*');
    });
    </script>
    """,
    height=0,
)

# Handle the submitted message
if user_input:
    response = f"You asked: {user_input}\nThis is a placeholder response. Implement actual data processing here."
    st.text_area("Response:", value=response, height=100)

# Additional styles for the layout
st.markdown("""
<style>
    .stMarkdown div {
        display: inline-block;
        margin: 8px;
    }
</style>
""", unsafe_allow_html=True)
