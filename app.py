import streamlit as st

# Streamlit app layout
st.title('CLV FPSO Layout')

# Define the layout with positions and dimensions for additional boxes
modules = {
    'M110': (1, 2), 'M111': (1, 3), 'M112': (2, 2), 'M113': (2, 3),
    'M120': (3, 2), 'M121': (3, 3), 'M122': (4, 2), 'M123': (4, 3),
    'M124': (5, 2), 'M125': (5, 3), 'M126': (6, 2), 'M115': (6, 3)
}

# Create the layout with specified colors and adjustments
layout = '''
<div style='border: 4px solid black; background-color: white; border-radius: 10px; padding: 20px; display: grid; grid-template-columns: repeat(4, 1fr); grid-gap: 20px; justify-items: center;'>
'''

# Adding additional boxes at each end
layout += '''
<div style='grid-column: 1 / span 4; background-color: white; height: 50px; border: 2px solid black; text-align: center; border-radius: 10px;'>LQ</div>
<div style='grid-column: 1 / span 4; background-color: white; height: 50px; border: 2px solid black; text-align: center; border-radius: 10px;'>HELI DECK</div>
'''

for module, (row, col) in modules.items():
    layout += f"<div style='grid-column: {col}; grid-row: {row}; background-color: black; color: white; padding: 20px; text-align: center; border: 2px solid white;'>{module}</div>"

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