import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d
import matplotlib.patheffects as path_effects
import numpy as np
import os

dbdir = r'F:\Assemblies\ErgoMaster\Assembly Manuals\EM153\GLB\test'
os.chdir(dbdir)
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def MakeBox1(x, y, z, Lx, Ly, Lz, Ox, Oy, Oz, Tx, Ty, Tz, facecolor, ax, text, zorder, alpha):
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
        faces, facecolor=facecolor, edgecolor='black', linewidths=1.5, alpha=alpha, zorder=zorder
    )
    if zorder < 10:
        mesh.set_zsort('min')
    else:
        mesh.set_zsort('max')
    ax.add_collection3d(mesh)

    # --- Add text on front face (z = 0) ---
    text_x = x + (Lx / 2) + Tx
    text_y = y + (Ly / 2) - 30 + Ty
    text_z = z + (Lz / 2) + Tz # front face at z = 0
    #text_pos = [text_x, text_y, text_z]
    text_label = ax.text(
                 text_x, text_y, text_z,
                 text,
                 color='white',
                 fontsize=14,
                 ha='center',
                 va='center',
                 zorder=999999999
                 #zdir='z'  # text facing outward along z-axis
             )
    # Add stroke (outline) around text
    text_label.set_path_effects([
        path_effects.Stroke(linewidth=2.5, foreground='black'),
        path_effects.Normal()
    ])


def save_shop_fig_v1(input_location):
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111, projection='3d')
    init_val = 0
    #####################################################################################################
    #       Shop Floor
    #####################################################################################################
    ax.plot([-100, 600, 600, -100, -100], [-100, -100, 500, 500, -100], color='black')
    text_label = ax.text(
        300, 500, 0,
        'MACHINE SHOP',
        color='white',
        fontsize=20,
        ha='center',
        va='center',
        zorder=999999999,
        zdir='x'  # text facing outward along z-axis
    )
    # Add stroke (outline) around text
    text_label.set_path_effects([
        path_effects.Stroke(linewidth=2.5, foreground='black'),
        path_effects.Normal()
    ])
    text_label = ax.text(
        -100, 200, 0,
        'ASSEMBLY TABLES',
        color='white',
        fontsize=20,
        ha='center',
        va='center',
        zorder=999999999,
        zdir='y'  # text facing outward along z-axis
    )
    # Add stroke (outline) around text
    text_label.set_path_effects([
        path_effects.Stroke(linewidth=2.5, foreground='black'),
        path_effects.Normal()
    ])
    for i in range(0, 2):
        for j in range(0, 2):
            for k in range(0, 2):
                x = -i*36 - 200
                y = j*250
                z = k*20
                MakeBox1(x, y, z,
                         36, 250, 20,
                         0, 0, 0,
                         0, 0, 0,
                         'white', ax, "", 100, 1)
    #####################################################################################################
    #       Ergo Master and Ergo I shelves
    #####################################################################################################
    shelves = ['EM2', 'EM1', 'EI1']
    Ox, Oy, Oz = 0, 0, 0
    Tx, Ty, Tz = 0, 0, 0
    facecolor = 'white'
    Lx, Ly, Lz = 24, 36, 18  # length (x), width (y), height (z)
    Sx = 6 # space between shelves
    s_cols = [5, 5, 5]
    s_rows = [4, 4, 4]
    Ss = 0
    for k in range(0, len(shelves)):
        So = Ss
        for i in range(0, s_cols[k]):
            for j in range(0, s_rows[k]):
                x = i*Lx + Ss + Ox
                y = Oy
                z = j*Lz + Oz
                alpha = alphabet[i]
                location = f'{shelves[k]}-{alpha}{j}'
                text = f'{alpha}{j}'
                text = ""
                facecolor = 'white'
                if input_location.split('-')[0] == shelves[k]:
                    facecolor = 'gray'
                if location == input_location:
                    facecolor = 'red'
                    init_val = 1
                MakeBox1(x, y, z, Lx, Ly, Lz, Ox, Oy, Oz, Tx, Ty, Tz, facecolor, ax, text, 100, 1)
        # --- Add text on front face (z = 0) ---
        Ss = Ss + (s_cols[k - 1] * Lx) + Sx
        text_x = (So + Ss) / 2
        text_y = 0
        text_z = -20  # front face at z = 0
        shelf_text = f'{shelves[k]}'
        if input_location.split('-')[0] not in shelves:
            shelf_text = ""
        text_label = ax.text(
                     text_x, text_y, text_z,
                     shelf_text,
                     color='white',
                     fontsize=20,
                     ha='center',
                     va='center',
                     zorder=999999999
                     #zdir='z'  # text facing outward along z-axis
                 )
        # Add stroke (outline) around text
        text_label.set_path_effects([
            path_effects.Stroke(linewidth=2.5, foreground='black'),
            path_effects.Normal()
        ])
    #####################################################################################################
    #       Roller Shelves
    #####################################################################################################
    shelves = ['ER3', 'ER2', 'ER1']
    Ox, Oy, Oz = 500, 0, 0
    Tx, Ty, Tz = -30, 36, 0
    facecolor = 'white'
    Lx, Ly, Lz = 36, 24, 18  # length (x), width (y), height (z)
    Sx = 6 # space between shelves
    s_cols = [6, 4, 5]
    s_rows = [6, 6, 7]
    Ss = Oy
    for k in range(0, len(shelves)):
        So = Ss
        for i in range(0, s_cols[k]):
            for j in range(0, s_rows[k]):
                x = Ox
                y = i*Ly + Ss + Oy
                z = j*Lz + Oz
                alpha = alphabet[s_cols[k]-1-i]
                location = f'{shelves[k]}-{alpha}{j}'
                text = f'{alpha}{j}'
                text = ""
                facecolor = 'white'
                if input_location.split('-')[0] == shelves[k]:
                    facecolor = 'gray'
                if location == input_location:
                    facecolor = 'red'
                    init_val = 2
                MakeBox1(x, y, z, Lx, Ly, Lz, Ox, Oy, Oz, Tx, Ty, Tz, facecolor, ax, text, 100, 1)
        # --- Add text on front face (z = 0) ---
        Ss = Ss + (s_cols[k] * Ly) + Sx
        text_x = Ox + -18
        text_y = ((So + Ss) / 2) + Oy +24
        text_z = -20  # front face at z = 0
        shelf_text = f'{shelves[k]}'
        if input_location.split('-')[0] not in shelves:
            shelf_text = ""
        text_label = ax.text(
                     text_x, text_y, text_z,
                     shelf_text,
                     color='white',
                     fontsize=20,
                     ha='center',
                     va='center',
                     zorder=999999999
                     #zdir='z'  # text facing outward along z-axis
                 )
        # Add stroke (outline) around text
        text_label.set_path_effects([
            path_effects.Stroke(linewidth=2.5, foreground='black'),
            path_effects.Normal()
        ])
    #####################################################################################################
    #       EF and ET shelves
    #####################################################################################################
    shelves = ['ET3', 'ET2', 'ET1', 'EF1']
    Ox, Oy, Oz = 0, 100, 0
    Tx, Ty, Tz = 0, 50, 0
    facecolor = 'white'
    Lx, Ly, Lz = 24, 36, 18  # length (x), width (y), height (z)
    Sx = 6 # space between shelves
    s_cols = [3, 3, 4, 5]
    s_rows = [5, 5, 5, 4]
    Ss = Ox
    box_num = 0
    for k in range(0, len(shelves)):
        So = Ss
        for i in range(0, s_cols[k]):
            for j in range(0, s_rows[k]):
                box_num = box_num + 1
                x = i*Lx + Ss + Ox
                y = Oy
                z = j*Lz + Oz
                alpha = alphabet[s_cols[k]-1-i]
                location = f'{shelves[k]}-{alpha}{j}'
                text = f'{alpha}{j}'
                text = f""
                facecolor = 'white'
                if input_location.split('-')[0] == shelves[k]:
                    facecolor = 'gray'
                if location == input_location:
                    facecolor = 'red'
                    init_val = 3
                MakeBox1(x, y, z, Lx, Ly, Lz, Ox, Oy, Oz, Tx, Ty, Tz, facecolor, ax, text, 100, 1)
        # --- Add text on front face (z = 0) ---
        Ss = Ss + (s_cols[k] * Lx) + Sx
        text_x = (So + Ss) / 2 + 12
        text_y = Oy + 36
        text_z = -20  # front face at z = 0
        shelf_text = f'{shelves[k]}'
        if input_location.split('-')[0] not in shelves:
            shelf_text = ""
        text_label = ax.text(
                     text_x, text_y, text_z,
                     shelf_text,
                     color='white',
                     fontsize=20,
                     ha='center',
                     va='center',
                     zorder=999999999
                     #zdir='z'  # text facing outward along z-axis
                 )
        # Add stroke (outline) around text
        text_label.set_path_effects([
            path_effects.Stroke(linewidth=2.5, foreground='black'),
            path_effects.Normal()
        ])
    #####################################################################################################
    #       Show Plot
    #####################################################################################################
    ax.set_aspect('equal')
    ax.dist = 1
    ax.view_init(elev=23, azim=-130)
    if init_val == 1:
        ax.view_init(elev=23, azim=-130)
    if init_val == 2:
        ax.view_init(elev=23, azim=-130)
    if init_val == 3:
        ax.view_init(elev=23, azim=130)
    # Remove all whitespace and margins
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.patch.set_alpha(0)           # transparent background (optional)
    ax.margins(0)
    ax.set_position([0, 0, 1, 1])    # fill the entire figure
    ax.grid(False)
    ax.set_axis_off()
    #ax.plot([-100, 600, 600, -100, -100], [-100, -100, 500, 500, -100], color='black')
    ax.set_xlim(-250, 610)
    ax.set_ylim(-110, 510)
    ax.set_zlim(-1, 150)
    #mng = plt.get_current_fig_manager()
    #mng.full_screen_toggle()
    plt.tight_layout()
    plt.savefig(f'{input_location}.png', dpi=200, bbox_inches='tight')
    #plt.show()


def execute_shop_imgs(shelf, cols, rows):
    locations = []
    for i in range(0, cols):
        for j in range(0, rows):
            locations.append(f'{shelf}-{alphabet[i]}{j}')
    for location in locations:
        print(location)
        save_shop_fig_v1(location)
        plt.close()


def save_bins_fig_v1(input_location, bin_bool):
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111, projection='3d')
    init_val = 20
    row = "Z"
    col = 100
    if bin_bool:
        row = input_location[:1]
        col = int(input_location[1:])
        print(f'{row}, {col}')
    #####################################################################################################
    #       Red Bin Dividers
    #####################################################################################################
    ax.plot([5, 5],[0, 0],[5,-55], color='black', linewidth=5, zorder=9999999)
    ax.plot([53.5, 53.5], [0, 0], [5, -55], color='black', linewidth=5, zorder=9999999)
    ax.plot([101.5, 101.5], [0, 0], [5, -55], color='black', linewidth=5, zorder=9999999)
    ax.plot([149, 149], [0, 0], [5, -55], color='black', linewidth=5, zorder=9999999)
    ax.plot([5, 149], [0, 0], [5.5, 5.5], color='black', linewidth=5, zorder=9999999)
    ax.plot([5, 149], [0, 0], [-24.5, -24.5], color='black', linewidth=5, zorder=9999999)
    ax.plot([5, 149], [0, 0], [-54.5, -54.5], color='black', linewidth=5, zorder=9999999)
    #####################################################################################################
    #       Red Bins
    #####################################################################################################
    Ox, Oy, Oz = 0, 0, 0
    Tx, Ty, Tz = 0, 0, 0
    facecolor = 'white'
    Lx, Ly, Lz = 5, 20, 5  # length (x), width (y), height (z)
    Sx = 1 # space between shelves
    bin = 0
    for i in range(1, 25):
        for j in range(0, 10):
            facecolor = 'white'
            bin = bin+1
            x = i * (Sx + Lx)
            y = 0
            z = -j * (Lz + Sx)
            if (i) == col:
                facecolor = 'yellow'
            if alphabet[j] == row:
                facecolor = 'yellow'
            if f'{alphabet[j]}{i}' == input_location:
                facecolor = 'red'
                Tx = x
                Tz = z
            MakeBox1(x, y, z, Lx, Ly, Lz, Ox, Oy, Oz, Tx, Ty, Tz, facecolor, ax, f"", 100, 1)

    #####################################################################################################
    #       Red Bins
    #####################################################################################################
    for i in range(25, 26):
        for j in range(6, 10):
            facecolor = 'white'
            bin = bin+1
            x = i * (Sx + Lx)
            y = 0
            z = -j * (Lz + Sx)
            MakeBox1(x, y, z, 24, Ly, Lz, Ox, Oy, Oz, Tx, Ty, Tz, facecolor, ax, f"", 100, 1)

    text_label = ax.text(
        Tx+3, 0, -58,
        f'{col}',
        color='white',
        fontsize=20,
        ha='center',
        va='center',
        zorder=999999999
        # zdir='z'  # text facing outward along z-axis
    )
    # Add stroke (outline) around text
    text_label.set_path_effects([
        path_effects.Stroke(linewidth=2.5, foreground='black'),
        path_effects.Normal()
    ])
    text_label = ax.text(
        0, 0, Tz+2.5,
        f'{row}',
        color='white',
        fontsize=20,
        ha='center',
        va='center',
        zorder=999999999
        # zdir='z'  # text facing outward along z-axis
    )
    # Add stroke (outline) around text
    text_label.set_path_effects([
        path_effects.Stroke(linewidth=2.5, foreground='black'),
        path_effects.Normal()
    ])

    #####################################################################################################
    #       Show Plot
    #####################################################################################################
    ax.set_aspect('equal')
    ax.dist = 1
    ax.view_init(elev=15, azim=-60)
    if init_val == 1:
        ax.view_init(elev=23, azim=-130)
    if init_val == 2:
        ax.view_init(elev=23, azim=-130)
    if init_val == 3:
        ax.view_init(elev=23, azim=130)
    # Remove all whitespace and margins
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.patch.set_alpha(0)           # transparent background (optional)
    ax.margins(0)
    ax.set_position([0, 0, 1, 1])    # fill the entire figure
    ax.grid(False)
    ax.set_axis_off()
    #ax.set_xlim(-250, 610)
    #ax.set_ylim(-110, 510)
    #ax.set_zlim(-1, 150)
    #mng = plt.get_current_fig_manager()
    #mng.full_screen_toggle()
    plt.tight_layout()
    plt.savefig(f'{input_location}.png', dpi=200, bbox_inches='tight')
    plt.show()



def save_EL_fig_v1(input_location):
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111, projection='3d')
    init_val = 20
    row = "Z"
    col = 100
    #####################################################################################################
    #       Red Bin Dividers
    #####################################################################################################
    ax.plot([5, 5],[0, 0],[-6,-55], color='black', linewidth=5, zorder=9999999)
    ax.plot([53.5, 53.5], [0, 0], [-6, -55], color='black', linewidth=5, zorder=9999999)
    ax.plot([101.5, 101.5], [0, 0], [-6, -55], color='black', linewidth=5, zorder=9999999)
    ax.plot([149, 149], [0, 0], [-6, -55], color='black', linewidth=5, zorder=9999999)
    ax.plot([5, 149], [0, 0], [-6, -6], color='black', linewidth=5, zorder=9999999)
    ax.plot([5, 149], [0, 0], [-24.5, -24.5], color='black', linewidth=5, zorder=9999999)
    ax.plot([5, 149], [0, 0], [-54.5, -54.5], color='black', linewidth=5, zorder=9999999)
    #####################################################################################################
    #       Red Bins
    #####################################################################################################
    Ox, Oy, Oz = 0, 0, 0
    Tx, Ty, Tz = 0, 0, 0
    facecolor = 'white'
    Lx, Ly, Lz = 5, 20, 5  # length (x), width (y), height (z)
    Sx = 1 # space between shelves
    bin = 0
    for i in range(1, 25):
        for j in range(2, 10):
            facecolor = 'white'
            bin = bin+1
            x = i * (Sx + Lx)
            y = 0
            z = -j * (Lz + Sx)
            if (i) == col:
                facecolor = 'yellow'
            if alphabet[j] == row:
                facecolor = 'yellow'
            if f'{alphabet[j]}{i}' == input_location:
                facecolor = 'red'
                Tx = x
                Tz = z
            MakeBox1(x, y, z, Lx, Ly, Lz, Ox, Oy, Oz, Tx, Ty, Tz, facecolor, ax, f"", 100, 1)


    #####################################################################################################
    #       Show Plot
    #####################################################################################################
    ax.set_aspect('equal')
    ax.dist = 1
    ax.view_init(elev=15, azim=-60)
    if init_val == 1:
        ax.view_init(elev=23, azim=-130)
    if init_val == 2:
        ax.view_init(elev=23, azim=-130)
    if init_val == 3:
        ax.view_init(elev=23, azim=130)
    # Remove all whitespace and margins
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.patch.set_alpha(0)           # transparent background (optional)
    ax.margins(0)
    ax.set_position([0, 0, 1, 1])    # fill the entire figure
    ax.grid(False)
    ax.set_axis_off()
    #ax.set_xlim(-250, 610)
    #ax.set_ylim(-110, 510)
    #ax.set_zlim(-1, 150)
    #mng = plt.get_current_fig_manager()
    #mng.full_screen_toggle()
    plt.tight_layout()
    plt.savefig(f'{input_location}.png', dpi=200, bbox_inches='tight')
    plt.show()




#save_bins_fig_v1('C10', True)

save_EL_fig_v1('EHFJKDASH')



