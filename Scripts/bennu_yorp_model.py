import trimesh
import numpy as np

# Loading mesh and scale/center
mesh = trimesh.load("data/bennu_model.obj")
if mesh.extents[0] < 10:
    mesh.apply_scale(1000.0)

mesh.vertices -= mesh.center_mass

# Physical Constants & Optical Properties for Bennu
P_sun = 4.56e-6 # Solar radiation pressure at 1 AU (N/m²)
s_hat = np.array([1.0, 0.0, 0.0])  # Sun vector (+X)

albedo = 0.044 # Bennu's Bond albedo (~4.4% reflective)
B_spec = 0.0 # Specular fraction (negligible for rough regolith)
B_diff = 1.0 # Diffuse reflection fraction (Lambertian scattering)

# 3. Extract mesh properties
normals = mesh.face_normals # (N, 3)
areas = mesh.area_faces # (N,) 

# Angle of incidence (cos_theta)
cos_theta = np.dot(normals, s_hat)
illuminated = cos_theta > 0.08

# Calculateing Force components per face (Optical + Thermal)
# Direct absorption & specular push along incoming light vector
# Diffuse scattering and thermal re-radiation push along face normal (-n_hat)
n_illuminated = normals[illuminated]
a_illuminated = areas[illuminated]
c_illuminated = cos_theta[illuminated]

# --- DECOUPLED FORCE CALCULATIONS ---
# Component 1: Direct Solar Radiation Pressure (acts along sun_vector)
F_srp = -P_sun * a_illuminated[:, np.newaxis] * c_illuminated[:, np.newaxis] * s_hat

# Component 2: Thermal Recoil Force (acts along normal vectors)
F_trf = -(2.0 / 3.0) * (1.0 - albedo) * P_sun * a_illuminated[:, np.newaxis] * c_illuminated[:, np.newaxis] * n_illuminated

# Total Net Force per Facet
face_forces = F_srp + F_trf

# Summing net force
total_yorp_force = np.sum(face_forces, axis=0)

print("=== Bennu Reflection & Thermal Re-radiation Engine ===")
print(f"Total Force Vector (N): {total_yorp_force}")
print(f"Total Force Magnitude: {np.linalg.norm(total_yorp_force):.6f} N")