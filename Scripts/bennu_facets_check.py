import trimesh
import numpy as np

# Loading mesh and scaling to meters
mesh = trimesh.load("data/bennu_model.obj")
if mesh.extents[0] < 10:
    mesh.apply_scale(1000.0)

# Re-centering to origin
mesh.vertices -= mesh.center_mass

# Extracting face normals and face areas
face_normals = mesh.face_normals # Array of shape (N, 3) representing unit vectors
face_areas = mesh.area_faces # Array of shape (N,) representing area in m²

total_surface_area = mesh.area

print("=== Bennu Facets & Normal Extraction Check ===")
print(f"Total Triangles (Faces): {len(mesh.faces):,}")
print(f"Total Surface Area: {total_surface_area:,.2f} m²")
print(f"Average Face Area: {np.mean(face_areas):.4f} m²")
print(f"Sample Face Normal [0]: {face_normals[0]}")