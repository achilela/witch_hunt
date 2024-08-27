import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
 
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
 
# Streamlit app layout
st.title('CLV FPSO Layout')
 
# Define the layout modules and positions
modules = {
    'M110': (0.5, 1), 'M111': (0.5, 2), 'M112': (0.5, 3), 'M113': (0.5, 4),
    'M114': (0.5, 5), 'M115': (0.5, 6), 'M116': (0.5, 7), 'M120': (2, 1),
    'M121': (2, 2), 'M122': (2, 3), 'M123': (2, 4), 'M124': (2, 5),
    'M125': (2, 6), 'M126': (2, 7)
}
 
racks = {
    'P-RACK 141': (1.5, 1), 'P-RACK 142': (1.5, 2), 'P-RACK 143': (1.5, 3),
    'P-RACK 144': (1.5, 4), 'P-RACK 145': (1.5, 5), 'P-RACK 146': (1.5, 6)
}
 
# Create a figure and axis for the layout
fig, ax = plt.subplots(figsize=(12, 8))
 
# Set the axis limits and aspect ratio
ax.set_xlim(0, 8)
ax.set_ylim(0, 2.5)
ax.set_aspect('equal')
 
# Draw the M modules
for module, (row, col) in modules.items():
    add_chamfered_rectangle(ax, (col, row), 1, 1, 0.1, edgecolor='black', facecolor='white')
    ax.text(col + 0.5, row + 0.5, module, ha='center', va='center', fontsize=10)
 
# Draw the RACK modules
for rack, (row, col) in racks.items():
    width = 0.25 if rack == 'P-RACK 146' else 0.15
    add_chamfered_rectangle(ax, (col, row), width, 1, 0.05, edgecolor='black', facecolor='white')
    ax.text(col + width / 2, row + 0.5, rack, ha='center', va='center', fontsize=8)
 
# Display the figure
st.pyplot(fig)
 
# Additional styles for the layout
st.markdown("""
<style>
    .stMarkdown div {
        display: inline-block;
        margin: 8px;
    }
</style>
""", unsafe_allow_html=True)
