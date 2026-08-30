import trimesh
import numpy as np

# Loading mesh, scale to meters, center mass
mesh = trimesh.load("data/bennu_model.obj")
if mesh.extents[0] < 10:
    mesh.apply_scale(1000.0)
mesh.vertices -= mesh.center_mass

# Physical Constants & Optical Parameters
P_sun = 4.56e-6 # Solar radiation pressure at 1 AU (N/m²)
s_hat = np.array([1.0, 0.0, 0.0])  # Sun vector (+X)

albedo = 0.044 # Bennu Bond albedo
B_spec = 0.0
B_diff = 1.0

# Extracting mesh properties
normals = mesh.face_normals # (N, 3)
areas = mesh.area_faces # (N,)
centroids = mesh.triangles.mean(axis=1) # Position vector r_i of each face centroid (N, 3)

# Angle of incidence (cos_theta)
cos_theta = np.dot(normals, s_hat)
illuminated = cos_theta > 0

# Calculating force vectors on illuminated faces
n_illum = normals[illuminated]
a_illum = areas[illuminated]
c_illum = cos_theta[illuminated]
r_illum = centroids[illuminated] # Position vectors for illuminated faces

f_normal_coeff = (2/3) * albedo * B_diff + (2/3) * (1 - albedo)
force_s = -(1 - albedo * B_spec) * s_hat[np.newaxis, :]
force_n = -f_normal_coeff * n_illum

# Force vector per illuminated face (N, 3)
face_forces = P_sun * a_illum[:, np.newaxis] * c_illum[:, np.newaxis] * (force_s + force_n)

# Calculating Torque per face: tau_i = r_i x F_i
face_torques = np.cross(r_illum, face_forces)

# Summing net force and torque vectors
total_force = np.sum(face_forces, axis=0)
total_torque = np.sum(face_torques, axis=0)

print("=== Bennu YORP Torque Engine ===")
print(f"Total Net Force (N): {total_force}")
print(f"Total Net Torque (N·m): {total_torque}")
print(f"Torque Magnitude (N·m): {np.linalg.norm(total_torque):.6e} N·m")