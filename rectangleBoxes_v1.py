import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d
import matplotlib.patheffects as path_effects
import numpy as np


def MakeBox(x, y, z, Lx, Ly, Lz, facecolor, ax):
    # --- box dimensions (edit these for a rectangular prism) ---
    #Lx, Ly, Lz = 24, 36, 18  # length (x), width (y), height (z)

    # Vertices
    v = [
        (x, y, z), (x+Lx, y, z), (x+Lx, y+Ly, z), (x, y+Ly, z),
        (x, y, z+Lz), (x+Lx, y, z+Lz), (x+Lx, y+Ly, z+Lz), (x, y+Ly, z+Lz)
    ]

    # Faces (each as a list of vertex tuples)
    faces = [
        [v[i] for i in [0, 1, 2, 3]],  # bottom
        [v[i] for i in [4, 5, 6, 7]],  # top
        [v[i] for i in [0, 1, 5, 4]],  # front
        [v[i] for i in [2, 3, 7, 6]],  # back
        [v[i] for i in [1, 2, 6, 5]],  # right
        [v[i] for i in [0, 3, 7, 4]]  # left
    ]

    # Draw faces (solid red) with black edges
    mesh = Poly3DCollection(
        faces, facecolor=facecolor, edgecolor='black', linewidths=1.5, alpha=1.0
    )
    ax.add_collection3d(mesh)

    # --- Add text on front face (z = 0) ---
    text_x = x + (Lx / 2)
    text_y = y + (Ly / 2) - 30
    text_z = z + (Lz / 2)  # front face at z = 0
    text_pos = [text_x, text_y, text_z]
    text_label = ax.text(
                 text_x, text_y, text_z,
                 'EI1-A2',
                 color='white',
                 fontsize=14,
                 ha='center',
                 va='center'
                 #zdir='z'  # text facing outward along z-axis
             )
    # Add stroke (outline) around text
    text_label.set_path_effects([
        path_effects.Stroke(linewidth=2.5, foreground='black'),
        path_effects.Normal()
    ])

Lx, Ly, Lz = 24, 36, 18  # length (x), width (y), height (z)

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')


for i in range(0, 5):
    x = i*Lx
    if i == 2:
        facecolor = 'red'
    else:
        facecolor = 'gray'
    MakeBox(x, 0, 0, Lx, Ly, Lz, facecolor, ax)


ax.set_aspect('equal')

# (Optional) axis labels; remove if you want a clean render
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.grid(False)

plt.tight_layout()
plt.savefig('red_box.png', dpi=200, bbox_inches='tight')
plt.show()


ax.view_init(elev=35, azim=135)


# Clean up axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.grid(False)

plt.tight_layout()
plt.show()
