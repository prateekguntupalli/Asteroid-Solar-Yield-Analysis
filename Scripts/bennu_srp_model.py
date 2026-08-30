import trimesh
import numpy as np

# Loading mesh and scaling to meters
mesh = trimesh.load("data/bennu_model.obj")
if mesh.extents[0] < 10:
    mesh.apply_scale(1000.0)

mesh.vertices -= mesh.center_mass

# Defining physical constants & solar vector
P_sun = 4.56e-6 # Solar radiation pressure at 1 AU (N/m²)
s_hat = np.array([1.0, 0.0, 0.0]) # Sunlight direction vector

# Extracting face properties
normals = mesh.face_normals # (N, 3)
areas = mesh.area_faces # (N,)

# Calculating illumination angle (dot product: cos(theta))
cos_theta = np.dot(normals, s_hat)

# Filtering for illuminated faces only (facing the sun: cos(theta) > 0)
illuminated = cos_theta > 0

# Computing elemental force per face (absorbed component)
# F_i = -P_sun * Area_i * cos(theta_i) * s_hat
force_magnitudes = P_sun * areas[illuminated] * cos_theta[illuminated]
force_vectors = -force_magnitudes[:, np.newaxis] * s_hat

# Summing total force vector
total_srp_force = np.sum(force_vectors, axis=0)

print("=== Bennu SRP Acceleration Engine ===")
print(f"Sun Vector (s_hat): {s_hat}")
print(f"Illuminated Facets: {np.sum(illuminated):,} / {len(mesh.faces):,}")
print(f"Total SRP Force Vector: {total_srp_force} N")
print(f"Total Force Magnitude: {np.linalg.norm(total_srp_force):.6f} N")