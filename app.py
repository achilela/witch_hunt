import streamlit as st

# Streamlit app layout
st.title('CLV FPSO Layout')

# Define the layout
modules = {
    'M110': (1, 1), 'M111': (1, 2), 'M112': (1, 3),
    'M113': (1, 4), 'M114': (1, 5), 'M115': (1, 6),
    'M116': (1, 7), 'M120': (2, 1), 'M121': (2, 2),
    'M122': (2, 3), 'M123': (2, 4), 'M124': (2, 5),
    'M125': (2, 6), 'M126': (2, 7)
}

# Create the layout with specified colors and adjustments
layout = '''
<div style='display: flex; flex-direction: column; align-items: center;'>
    <div style='border: 8px solid black; border-radius: 10px; background-color: white; padding: 30px; display: grid; grid-template-columns: repeat(7, 1fr); grid-gap: 40px;'>
'''

for module, (row, col) in modules.items():
    layout += f"<div style='grid-column: {col}; grid-row: {row}; background-color: black; color: white; padding: 20px; text-align: center; border: 2px solid white; border-radius: 10px;'>{module}</div>"

layout += '''
    </div>
    <div style='display: flex; justify-content: flex-end; width: 100%; margin-top: -210px;'>
        <div style='border: 8px solid black; border-radius: 10px; background-color: white; padding: 30px; text-align: center; width: 10%; margin-right: -90px;'>M131 Flare</div>
    </div>
</div>
'''

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
