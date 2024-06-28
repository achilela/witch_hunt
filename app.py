import streamlit as st

# Streamlit app layout
st.title('FPSO Layout')

# Define the layout and colors for each module
modules = {
    'M110': (1, 2, 'yellow'), 'M111': (1, 3, 'blue'), 'M112': (1, 4, 'blue'),
    'M113': (1, 5, 'blue'), 'M114': (1, 6, 'yellow'), 'M115': (1, 7, 'red'),
    'M116': (1, 8, 'red'), 'M120': (2, 2, 'yellow'), 'M121': (2, 3, 'yellow'),
    'M122': (2, 4, 'yellow'), 'M123': (2, 5, 'yellow'), 'M124': (2, 6, 'yellow'),
    'M125': (2, 7, 'yellow'), 'M126': (2, 8, 'yellow')
}

# Create the layout with specified colors
layout = '''
<div style='display: grid; grid-template-columns: repeat(8, 1fr); grid-gap: 10px;'>
'''

for module, (row, col, color) in modules.items():
    layout += f"<div style='grid-column: {col}; grid-row: {row}; background-color: {color}; padding: 20px; text-align: center;'>{module}</div>"

layout += '</div>'

st.markdown(layout, unsafe_allow_html=True)

# Additional styles for the layout
st.markdown("""
<style>
    .stMarkdown div {
        display: inline-block;
        margin: 10px;
    }
</style>
""", unsafe_allow_html=True)