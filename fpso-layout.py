import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import matplotlib.transforms as transforms

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
    # ... (rest of the draw_clv function)

def draw_paz(ax):
    ax.text(6, 1.75, "PAZ Layout\n(Not implemented)", ha='center', va='center', fontsize=16, weight='bold')

def draw_dal(ax):
    ax.text(6, 1.75, "DAL Layout\n(Not implemented)", ha='center', va='center', fontsize=16, weight='bold')

def draw_gir(ax):
    ax.text(6, 1.75, "GIR Layout\n(Not implemented)", ha='center', va='center', fontsize=16, weight='bold')

def draw_fpso_layout(selected_unit):
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
