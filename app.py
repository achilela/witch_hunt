import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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

# Create a figure and axis
fig, ax = plt.subplots()

# Draw the ship hull
ship_hull = patches.Rectangle((0, 0), 10, 5, linewidth=1, edgecolor='black', facecolor='none')
ax.add_patch(ship_hull)

# Draw the modules
for module, (row, col) in modules.items():
    module_rect = patches.Rectangle((col * 1.5, row * 2.5), 1, 1, linewidth=1, edgecolor='black', facecolor='black')
    ax.add_patch(module_rect)
    ax.text(col * 1.5 + 0.5, row * 2.5 + 0.5, module, ha='center', va='center', color='white')

# Draw the flare
flare = patches.Rectangle((7.5, 2.5), 2, 1, linewidth=1, edgecolor='black', facecolor='black')
ax.add_patch(flare)
ax.text(8.5, 2.5, 'M131 Flare', ha='center', va='center', color='white')

# Set the axis limits
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)

# Show the plot
st.pyplot(fig)

if __name__ == '__main__':
    st.run()
