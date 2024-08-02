import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
 
# Streamlit app layout
st.title('CLV FPSO Layout')
 
# Define the layout modules
modules = {
    'M110': (1, 1), 'M111': (1, 2), 'M112': (1, 3), 'M113': (1, 4),
    'M114': (1, 5), 'M115': (1, 6), 'M116': (1, 7), 'M120': (2, 1),
    'M121': (2, 2), 'M122': (2, 3), 'M123': (2, 4), 'M124': (2, 5),
    'M125': (2, 6), 'M126': (2, 7)
}
 
# Create a sidebar for shape selection
st.sidebar.header('Shape Selection')
shape_options = ['Rectangle', 'Triangle', 'Circle', 'Other']
selected_shape = st.sidebar.selectbox('Select a shape:', shape_options)
 
# Create a sidebar for shape properties
st.sidebar.header('Shape Properties')
shape_properties = {}
if selected_shape == 'Rectangle':
    shape_properties['width'] = st.sidebar.slider('Width:', 1, 10, 5)
    shape_properties['height'] = st.sidebar.slider('Height:', 1, 10, 5)
    shape_properties['color'] = st.sidebar.color_picker('Color:')
elif selected_shape == 'Triangle':
    shape_properties['base'] = st.sidebar.slider('Base:', 1, 10, 5)
    shape_properties['height'] = st.sidebar.slider('Height:', 1, 10, 5)
    shape_properties['color'] = st.sidebar.color_picker('Color:')
elif selected_shape == 'Circle':
    shape_properties['radius'] = st.sidebar.slider('Radius:', 1, 10, 5)
    shape_properties['color'] = st.sidebar.color_picker('Color:')
else:
    st.sidebar.write('Please select a shape')
 
# Create a figure and axis for the layout
fig, ax = plt.subplots(figsize=(10, 6))
 
# Draw the modules
for module, (row, col) in modules.items():
    ax.add_patch(patches.Rectangle((col, row), 1, 1, edgecolor='black', facecolor='white'))
    ax.text(col + 0.5, row + 0.5, module, ha='center', va='center')
 
# Draw the selected shape
if selected_shape == 'Rectangle':
    ax.add_patch(patches.Rectangle((0, 0), shape_properties['width'], shape_properties['height'], edgecolor='black', facecolor=shape_properties['color']))
elif selected_shape == 'Triangle':
    triangle = patches.Polygon([(0, 0), (shape_properties['base'], 0), (shape_properties['base']/2, shape_properties['height'])], edgecolor='black', facecolor=shape_properties['color'])
    ax.add_patch(triangle)
elif selected_shape == 'Circle':
    ax.add_patch(patches.Circle((0, 0), radius=shape_properties['radius'], edgecolor='black', facecolor=shape_properties['color']))
 
# Set the axis limits and aspect ratio
ax.set_xlim(0, 8)
ax.set_ylim(0, 3)
ax.set_aspect('equal')
 
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
 
