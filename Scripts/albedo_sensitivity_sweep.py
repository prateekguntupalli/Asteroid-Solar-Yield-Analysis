import pandas as pd

# Loading baseline 360-degree sweep dataset
df = pd.read_csv("Data/bennu_yorp_sweep_results.csv")
baseline_tau_z_1au = df['Tau_z'].mean()

# Baseline Bond albedo used in main simulation
albedo_baseline = 0.044

# Range of albedo values for sensitivity testing
albedo_range = [0.030, 0.044, 0.060]

albedo_results = []
for A in albedo_range:
    # Absorbed + Lambertian reflected force scaling: f_normal = 1 - (1/3)*A
    f_coeff_base = 1.0 - (1.0 / 3.0) * albedo_baseline
    f_coeff_new = 1.0 - (1.0 / 3.0) * A
    
    # Scaling torque based on modified diffuse recoil contribution
    scale = f_coeff_new / f_coeff_base
    tau_z_val = baseline_tau_z_1au * scale
    
    albedo_results.append({
        'bond_albedo': A,
        'mean_tau_z_Nm': tau_z_val,
        'pct_change_from_baseline': ((tau_z_val - baseline_tau_z_1au) / baseline_tau_z_1au) * 100
    })

# Compiling results dataframe
df_albedo = pd.DataFrame(albedo_results)

# Saving and printing output
df_albedo.to_csv("Data/bennu_albedo_sweep_results.csv", index=False)

print("=== ALBEDO SENSITIVITY SWEEP RESULTS ===")
print(df_albedo.to_string(index=False))
print("\nExported results to 'bennu_albedo_sweep_results.csv'.")