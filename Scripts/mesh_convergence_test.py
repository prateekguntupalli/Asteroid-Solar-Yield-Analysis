import trimesh
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Physical Constants
P_sun = 4.56e-6 # Solar radiation pressure at 1 AU (N/m²)
albedo = 0.044 # Bennu Bond albedo
B_spec = 0.0
B_diff = 1.0
f_normal_coeff = (2/3) * albedo * B_diff + (2/3) * (1 - albedo)

# Loading full resolution base mesh
print("Loading base 3.36M mesh model...")
full_mesh = trimesh.load("data/bennu_model.obj")
if full_mesh.extents[0] < 10:
    full_mesh.apply_scale(1000.0)
full_mesh.vertices -= full_mesh.center_mass

# Defining target face counts for downsampling
target_face_counts = [10000, 50000, 100000, 500000, len(full_mesh.faces)]
convergence_results = []

def compute_daily_mean_tau_z(mesh_obj):
    normals = mesh_obj.face_normals
    areas = mesh_obj.area_faces
    centroids = mesh_obj.triangles.mean(axis=1)
    
    tau_z_list = []
    
    # 360-degree rotation sweep
    for angle_deg in range(0, 360):
        angle_rad = np.radians(angle_deg)
        s_hat = np.array([np.cos(angle_rad), np.sin(angle_rad), 0.0])
        
        cos_theta = np.dot(normals, s_hat)
        illuminated = cos_theta > 0
        
        n_illum = normals[illuminated]
        a_illum = areas[illuminated]
        c_illum = cos_theta[illuminated]
        r_illum = centroids[illuminated]
        
        force_s = -(1 - albedo * B_spec) * s_hat[np.newaxis, :]
        force_n = -f_normal_coeff * n_illum
        
        face_forces = P_sun * a_illum[:, np.newaxis] * c_illum[:, np.newaxis] * (force_s + force_n)
        face_torques = np.cross(r_illum, face_forces)
        
        total_torque = np.sum(face_torques, axis=0)
        tau_z_list.append(total_torque[2])
        
    return np.mean(tau_z_list)

print("Starting mesh resolution convergence sweep...")

for faces in target_face_counts:
    if faces == len(full_mesh.faces):
        print(f"Testing full resolution ({faces:,} facets)...")
        current_mesh = full_mesh
    else:
        print(f"Downsampling mesh to ~{faces:,} facets...")
        try:
            # Calculating reduction ratio between 0 and 1
            target_reduction = 1.0 - (faces / len(full_mesh.faces))
            current_mesh = full_mesh.simplify_quadric_decimation(target_reduction)
        except Exception as e:
            print(f"Quadric decimation failed ({e}). Using face sub-sampling fallback...")
            step = max(1, len(full_mesh.faces) // faces)
            faces_subset = np.arange(0, len(full_mesh.faces), step)
            current_mesh = full_mesh.submesh([faces_subset])[0]

        current_mesh.vertices -= current_mesh.center_mass

    mean_tau_z = compute_daily_mean_tau_z(current_mesh)
    actual_faces = len(current_mesh.faces)
    
    print(f"  -> Facets: {actual_faces:,} | Mean Tau_Z: {mean_tau_z:.6e} N·m")
    
    convergence_results.append({
        'face_count': actual_faces,
        'mean_tau_z': mean_tau_z
    })

# Saving convergence dataset
df_conv = pd.DataFrame(convergence_results)
df_conv.to_csv("bennu_mesh_convergence_results.csv", index=False)

# Plotting Convergence Curve
plt.style.use('seaborn-v0_8-paper' if 'seaborn-v0_8-paper' in plt.style.available else 'default')
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

ax.plot(df_conv['face_count'], df_conv['mean_tau_z'], marker='o', color='#1f77b4', linewidth=2, markersize=6)
ax.axhline(df_conv['mean_tau_z'].iloc[-1], color='red', linestyle='--', alpha=0.7, label='Full Mesh Baseline (3.36M)')

ax.set_xscale('log')
ax.set_xlabel('Mesh Facet Count (Log Scale)', fontsize=11, fontweight='bold')
ax.set_ylabel(r'Mean Daily YORP Torque $\bar{\tau}_z$ ($\mathrm{N \cdot m}$)', fontsize=11, fontweight='bold')
ax.set_title('YORP Net Torque Convergence vs. Mesh Resolution', fontsize=12, pad=12, fontweight='bold')
ax.grid(True, which="both", linestyle='--', alpha=0.5)
ax.legend(loc='lower right', frameon=True)

plt.tight_layout()
plt.savefig("bennu_resolution_convergence.png", dpi=300)
plt.close()

print("\n=== Convergence Test Complete ===")
print("Saved convergence plot to 'bennu_resolution_convergence.png'")