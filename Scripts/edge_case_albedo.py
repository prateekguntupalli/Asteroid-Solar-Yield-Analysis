import numpy as np

# Physical constants and baseline setup
P_sun = 4.56e-6 # Solar radiation pressure at 1 AU (N/m^2)
extreme_albedos = [0.010, 0.100] # Far beyond standard range [0.030, 0.060]

print("=== Extreme Albedo Bounds Sweep ===")
for A in extreme_albedos:
    # Optical response coefficients
    f_normal = (2.0 / 3.0) * A + (2.0 / 3.0) * (1.0 - A)
    f_shear = 1.0 - A

    # Scaling estimation relative to baseline (A_base = 0.044)
    tau_z_estimate = 0.014867 * (f_normal / 0.696)
    print(f"Albedo A = {A:.3f} | Normal Coeff: {f_normal:.4f} | Est. Tau_z: {tau_z_estimate:.6f} N*m")