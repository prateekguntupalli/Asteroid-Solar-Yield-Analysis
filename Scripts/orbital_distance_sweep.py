import pandas as pd

# Loading baseline 360-degree sweep dataset (calculated at 1 AU)
df = pd.read_csv("Data/bennu_yorp_sweep_results.csv")
baseline_tau_z_1au = df['Tau_z'].mean()

# Bennu orbital parameters (in Astronomical Units)
r_1au = 1.0 # Baseline distance
r_perihelion = 0.896 # Closest approach to Sun
r_aphelion = 1.355 # Farthest distance from Sun

# Inverse-square distance scaling: P_sun ∝ 1 / r²
tau_z_perihelion = baseline_tau_z_1au * (r_1au / r_perihelion)**2
tau_z_aphelion = baseline_tau_z_1au * (r_1au / r_aphelion)**2

# Compiling results dataframe
orbit_results = pd.DataFrame([
    {
        'orbital_position': 'Perihelion',
        'distance_au': r_perihelion,
        'mean_tau_z_Nm': tau_z_perihelion,
        'pct_change_from_1au': ((tau_z_perihelion - baseline_tau_z_1au) / baseline_tau_z_1au) * 100
    },
    {
        'orbital_position': '1 AU Baseline',
        'distance_au': r_1au,
        'mean_tau_z_Nm': baseline_tau_z_1au,
        'pct_change_from_1au': 0.0
    },
    {
        'orbital_position': 'Aphelion',
        'distance_au': r_aphelion,
        'mean_tau_z_Nm': tau_z_aphelion,
        'pct_change_from_1au': ((tau_z_aphelion - baseline_tau_z_1au) / baseline_tau_z_1au) * 100
    }
])

# Saving and printing output
orbit_results.to_csv("bennu_orbital_sweep_results.csv", index=False)

print("=== ORBITAL DISTANCE SWEEP RESULTS ===")
print(orbit_results.to_string(index=False))
print("\nExported results to 'bennu_orbital_sweep_results.csv'.")