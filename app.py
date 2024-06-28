import streamlit as st

# Streamlit app layout
st.title('CLV FPSO Layout')

# Define the layout
modules = {
    'M110': (1, 2), 'M111': (1, 3), 'M112': (1, 4),
    'M113': (1, 5), 'M114': (1, 6), 'M115': (1, 7),
    'M116': (1, 8), 'M120': (2, 2), 'M121': (2, 3),
    'M122': (2, 4), 'M123': (2, 5), 'M124': (2, 6),
    'M125': (2, 7), 'M126': (2, 8)
}

# Create the layout with specified colors and adjustments
layout = '''
<div style='display: flex; flex-direction: column; align-items: center;'>
    <div style='border: 4px solid black; border-radius: 10px; background-color: white; padding: 20px; display: grid; grid-template-columns: repeat(8, 1fr); grid-gap: 20px;'>
'''

for module, (row, col) in modules.items():
    layout += f"<div style='grid-column: {col}; grid-row: {row}; background-color: black; color: white; padding: 20px; text-align: center; border: 2px solid white; border-radius: 10px;'>{module}</div>"

layout += '''
    </div>
    <div style='margin-top: 20px; display: flex; justify-content: space-between; width: 95%;'>
        <div style='border: 2px solid black; border-radius: 10px; background-color: white; padding: 20px; text-align: center; width: 16%; margin-left: 103%;'>M131 Flare</div>
        <div style='flex: 1;'></div>
    </div>
    <div style='margin-top: 20px; display: flex; justify-content: space-between; width: 100%;'>
        <div style='border: 2px solid black; border-radius: 10px; background-color: white; padding: 20px; text-align: center; width: 16%;'>LQ</div>
        <div style='flex: 1;'></div>
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
