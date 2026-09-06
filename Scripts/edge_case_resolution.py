import trimesh

# Load full resolution baseline mesh
full_mesh = trimesh.load("Data/bennu_model.obj")

# Decimate mesh to 10,000 facets
target_facets = 10000
coarse_mesh = full_mesh.simplify_quadric_decimation(face_count=target_facets)

# Compute spatial metrics
faces = len(coarse_mesh.faces)
surface_area = coarse_mesh.area
volume = coarse_mesh.volume

# Surface area discrepancy relative to 3.36M baseline
area_loss = ((full_mesh.area - surface_area) / full_mesh.area) * 100

print("=== Coarse Mesh Degradation Check Output ===")
print(f"Target Facet Count: {target_facets:,}")
print(f"Actual Facet Count: {faces:,}")
print(f"Decimated Area: {surface_area:.2f} m^2 ({area_loss:.2f}% area loss)")
print(f"Decimated Volume: {volume:.2f} m^3")