import trimesh
import numpy as np

# Loading mesh and scaling to meters
mesh = trimesh.load("data/bennu_model.obj")
if mesh.extents[0] < 10:
    mesh.apply_scale(1000.0)

# Centering the mesh coordinates
mesh.vertices -= mesh.center_mass

# Calculating distance from (0,0,0) for all vertices
radial_distances = np.linalg.norm(mesh.vertices, axis=1)

min_radius = radial_distances.min()
max_radius = radial_distances.max()

# Computing equivalent volume spherical radius (R_eq = (3V / 4pi)^(1/3))
equivalent_radius = (3 * mesh.volume / (4 * np.pi)) ** (1/3)

print("=== Bennu Spatial Bounds Check ===")
print(f"Minimum Radius from CoM : {min_radius:.2f} m")
print(f"Maximum Radius from CoM : {max_radius:.2f} m")
print(f"Equivalent Mean Radius   : {equivalent_radius:.2f} m")