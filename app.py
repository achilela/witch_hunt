import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

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
    # Calculate vertices of the hexagon
    vertices = [(x + radius * math.cos(2 * math.pi * n / 6), 
                 y + radius * math.sin(2 * math.pi * n / 6)) 
                for n in range(6)]
    
    hexagon = patches.Polygon(vertices, closed=True, **kwargs)
    ax.add_patch(hexagon)

# Streamlit app layout
st.title('CLV')

# Define the layout modules and positions
modules = {
    'M120': (0.5, 2), 'M121': (0.5, 3), 'M122': (0.5, 4), 'M123': (0.5, 5),
    'M124': (0.5, 6), 'M125': (0.5, 7), 'M126': (0.5, 8), 'M110': (2, 2),
    'M111': (2, 3), 'M112': (2, 4), 'M113': (2, 5), 'M114': (2, 6),
    'M115': (2, 7), 'M116': (2, 8)
}

racks = {
    'P-RACK 141': (1.5, 2), 'P-RACK 142': (1.5, 3), 'P-RACK 143': (1.5, 4),
    'P-RACK 144': (1.5, 5), 'P-RACK 145': (1.5, 6), 'P-RACK 146': (1.5, 7)
}

flare = {
    'FLARE': (0.5, 9) 
}

living_quarters = {
    'LQ': (0.5, 1)
}

# Example hexagon to add
hexagons = {
    'HEX1': (4, 1.5)
}

# Create a figure and axis for the layout
fig, ax = plt.subplots(figsize=(12, 8))

# Set the axis limits and aspect ratio
ax.set_xlim(0, 12)
ax.set_ylim(0, 3.5)
ax.set_aspect('equal')

# Draw the M modules
for module, (row, col) in modules.items():
    add_chamfered_rectangle(ax, (col, row), 1, 1, 0.1, edgecolor='black', facecolor='white')
    ax.text(col + 0.5, row + 0.5, module, ha='center', va='center', fontsize=10)

# Draw the RACK modules
for rack, (row, col) in racks.items():
    width = 2 if rack == 'P-RACK 146' else 1
    add_chamfered_rectangle(ax, (col, row), width, 0.5, 0.05, edgecolor='black', facecolor='white')
    ax.text(col + width / 2, row + 0.25, rack, ha='center', va='center', fontsize=8)

# Draw the flare with chamfer only at the top
for flare, (row, col) in flare.items():
    add_chamfered_rectangle(ax, (col, row), 1, 2.5, 0.1, edgecolor='black', facecolor='white')
    ax.text(col + 0.5, row + 1.25, flare, ha='center', va='center', fontsize=10)

# Draw the LQ module
for living_quarter, (row, col) in living_quarters.items():
    add_rectangle(ax, (col, row), 1, 2.5, edgecolor='black', facecolor='white')
    ax.text(col + 0.5, row + 1.25, living_quarter, ha='center', va='center', fontsize=10, rotation=90)

# Draw the hexagons
for hexagon, (row, col) in hexagons.items():
    add_hexagon(ax, (col, row), 0.5, edgecolor='black', facecolor='white')
    ax.text(col, row, hexagon, ha='center', va='center', fontsize=10)

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
