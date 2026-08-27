import trimesh

#Loading the Bennu 3D mesh file from the data folder
mesh = trimesh.load("Data/bennu_model.obj")

#Scaling the model from kilometers to standard meters
if mesh.extents[0] < 10:
    mesh.apply_scale(1000.0)

#Printing the core geometry statistics
print("=== Bennu Geometry Statistics ===")
print(f"Total Vertices: {len(mesh.vertices):,}")
print(f"Total Faces: {len(mesh.faces):,}")
print(f"Is Watertight: {mesh.is_watertight}")
print(f"Bounding Box (meters): {mesh.extents}")
print(f"Total Surface Area (m²): {mesh.area:,.2f}")
print(f"Total Volume (m³): {mesh.volume:,.2f}")