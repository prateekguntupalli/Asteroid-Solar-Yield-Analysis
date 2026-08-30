import trimesh
import numpy as np
import pandas as pd

# Loading mesh, scale to meters, center mass
print("Loading mesh model...")
mesh = trimesh.load("data/bennu_model.obj")
if mesh.extents[0] < 10:
    mesh.apply_scale(1000.0)
mesh.vertices -= mesh.center_mass

# Physical Constants & Optical Properties
P_sun = 4.56e-6 # Solar radiation pressure at 1 AU (N/m²)
albedo = 0.044 # Bennu Bond albedo
B_spec = 0.0
B_diff = 1.0

normals = mesh.face_normals # (N, 3)
areas = mesh.area_faces # (N,)
centroids = mesh.triangles.mean(axis=1) # (N, 3)

# Normal recoil coefficient
f_normal_coeff = (2/3) * albedo * B_diff + (2/3) * (1 - albedo)

results = []

print("Executing 360-degree rotational sweep...")
# Sweep rotation angle theta around Z-axis in 1-degree increments
for angle_deg in range(0, 360):
    angle_rad = np.radians(angle_deg)
    
    # Sun vector s_hat rotating in the XY plane
    s_hat = np.array([np.cos(angle_rad), np.sin(angle_rad), 0.0])
    
    # Calculating incidence angles
    cos_theta = np.dot(normals, s_hat)
    illuminated = cos_theta > 0
    
    # Filtering for illuminated day-side facets
    n_illum = normals[illuminated]
    a_illum = areas[illuminated]
    c_illum = cos_theta[illuminated]
    r_illum = centroids[illuminated]
    
    # Calculating vector forces
    force_s = -(1 - albedo * B_spec) * s_hat[np.newaxis, :]
    force_n = -f_normal_coeff * n_illum
    
    face_forces = P_sun * a_illum[:, np.newaxis] * c_illum[:, np.newaxis] * (force_s + force_n)
    face_torques = np.cross(r_illum, face_forces)
    
    # Summing net vectors
    total_force = np.sum(face_forces, axis=0)
    total_torque = np.sum(face_torques, axis=0)
    
    results.append({
        'rotation_deg': angle_deg,
        'Fx': total_force[0],
        'Fy': total_force[1],
        'Fz': total_force[2],
        'Tau_x': total_torque[0],
        'Tau_y': total_torque[1],
        'Tau_z': total_torque[2],
        'Torque_Mag': np.linalg.norm(total_torque)
    })

# Saving to CSV
df = pd.DataFrame(results)
df.to_csv("bennu_yorp_sweep_results.csv", index=False)
print("Data collection complete! Exported to 'bennu_yorp_sweep_results.csv'.")