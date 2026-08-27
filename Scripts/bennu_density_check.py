import trimesh

# Loading the mesh and scaling to standard meters
mesh = trimesh.load("data/bennu_model.obj")
if mesh.extents[0] < 10:
    mesh.apply_scale(1000.0)

# Recording the original center of mass
initial_center = mesh.center_mass

# Re-centering the mesh so (0,0,0) is at the center of mass
mesh.vertices -= initial_center

#Computing bulk density using OSIRIS-REx estimated mass (~7.329e10 kg)
mass_kg = 7.329e10  # 73.29 million metric tons
bulk_density = mass_kg / mesh.volume

print("=== Bennu Center of Mass & Density Check ===")
print(f"Original Center of Mass: [{initial_center[0]:.4f}, {initial_center[1]:.4f}, {initial_center[2]:.4f}]")
print(f"New Center of Mass: [{mesh.center_mass[0]:.4f}, {mesh.center_mass[1]:.4f}, {mesh.center_mass[2]:.4f}]")
print(f"Calculated Bulk Density: {bulk_density:.2f} kg/m³")