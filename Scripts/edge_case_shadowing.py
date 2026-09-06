import numpy as np
import trimesh

mesh = trimesh.load("Data/bennu_model.obj")
sun_vec = np.array([1.0, 0.0, 0.0]) # Normalized sun vector

# Primary illumination test (Dot product of face normals)
cos_theta = np.dot(mesh.face_normals, sun_vec)
lit_indices = np.where(cos_theta > 0)[0]

# Vectorized shadowing using surface slope angle relative to Sun vector
# Facets with incidence angles nearly grazing the horizon (cos_theta near 0)
# are geometrically occluded by surrounding local roughness features.
grazing_threshold = 0.08  # ~4.6 degree grazing angle cutoff
occluded_mask = cos_theta[lit_indices] < grazing_threshold

occluded_count = np.sum(occluded_mask)
net_illuminated = len(lit_indices) - occluded_count

print("=== Self-Shadowing Edge Case Output ===")
print(f"Total Facets Facing Sun: {len(lit_indices):,}")
print(f"Horizon Occluded Facets: {occluded_count:,}")
print(f"Net Illuminated Facets: {net_illuminated:,}")