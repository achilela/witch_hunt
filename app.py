import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import matplotlib.transforms as transforms

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
    ax.text(0, -1, "FWD", ha='center', va='center', fontsize=7, transform=text_t + ax.transData)

# Streamlit app layout
st.title('CLV')

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

# Create a figure and axis for the layout
fig, ax = plt.subplots(figsize=(12, 8))

# Set the axis limits and aspect ratio
ax.set_xlim(0, 12)
ax.set_ylim(0, 3.5)
ax.set_aspect('equal')

# Draw the M modules
for module, (row, col) in modules.items():
    height = 1.25 if module == 'M110' else 1
    
    add_chamfered_rectangle(ax, (col, row), 1, height, 0.1, edgecolor='black', facecolor='white')
    ax.text(col + 0.5, row + 0.5, module, ha='center', va='center', fontsize=7)

# Draw the RACK modules
for rack, (row, col) in racks.items():
    width = 1 if rack == 'P-RACK 146' else 1
    add_chamfered_rectangle(ax, (col, row), width, 0.5, 0.05, edgecolor='black', facecolor='white')
    ax.text(col + width / 2, row + 0.25, rack, ha='center', va='center', fontsize=7)

# Draw the flare with chamfer only at the top
for flare, (row, col) in flare.items():
    add_chamfered_rectangle(ax, (col, row), 0.5, 2.5, 0.1, edgecolor='black', facecolor='white')
    ax.text(col + 0.25, row + 1.25, flare, ha='center', va='center', fontsize=7)

# Draw the LQ module
for living_quarter, (row, col) in living_quarters.items():
    add_rectangle(ax, (col, row), 1, 2.5, edgecolor='black', facecolor='white')
    ax.text(col + 0.5, row + 1.25, living_quarter, ha='center', va='center', fontsize=7, rotation=90)

# Draw the hexagons
for hexagon, (row, col) in hexagons.items():
    add_hexagon(ax, (col, row), 0.60, edgecolor='black', facecolor='white')
    ax.text(col, row, hexagon, ha='center', va='center', fontsize=7)

# Draw the FWD module
for fwd_module, (row, col) in fwd.items():
    add_fwd(ax, (col, row), 2.5, -1, edgecolor='black', facecolor='white')

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
