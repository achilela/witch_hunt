import streamlit as st
import pandas as pd
 
# Load the dataset
#data = pd.read_excel('/mnt/data/file-kXDunD43ReJ6svJG6mWYLb06.xlsx')
 
# Function to determine the color based on the dataset
#def get_module_color(module_code, anomaly_type):
#    try:
#        value = data.pivot_table(index=['Module Code', 'Anomaly Type'], values='Value').loc[(module_code, anomaly_type)]
#        if value > threshold_red:
#            return 'red'
#        elif value > threshold_amber:
#            return 'amber'
#        else:
#            return 'green'
#    except KeyError:
#        return 'green'
 
# Streamlit app layout
st.title('FPSO Layout')
 
# Define the layout
modules = {
    'M110': (1, 2), 'M111': (1, 3), 'M112': (1, 4),
    'M113': (1, 5), 'M114': (1, 6), 'M115': (1, 7),
    'M116': (1, 8), 'M120': (2, 2), 'M121': (2, 3),
    'M122': (2, 4), 'M123': (2, 5), 'M124': (2, 6),
    'M125': (2, 7), 'M126': (2, 8)
}
 
# Dropdown for selecting anomaly type
anomaly_type = st.selectbox('Select Anomaly Type', ['COA1', 'COA2', 'COA3', 'COA4', 'ICOA'])
 
# Display the modules in the layout
#for module, pos in modules.items():
#    color = get_module_color(module, anomaly_type)
#    st.markdown(f"<div style='grid-area: {pos[0]} / {pos[1]}; background-color: {color}; padding: 20px;'>{module}</div>", unsafe_allow_html=True)
 
# Additional styles and layout configurations
st.markdown("""
<style>
    .stMarkdown div {
        display: inline-block;
        margin: 10px;
    }
</style>
""", unsafe_allow_html=True)
