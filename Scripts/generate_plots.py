import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Setting clean aesthetic style for publication figures
plt.style.use('seaborn-v0_8-paper' if 'seaborn-v0_8-paper' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

# Loading dataset
df = pd.read_csv("Data/bennu_yorp_sweep_results.csv")

# Figure 1: Net Forces (Fx, Fy, Fz) vs. Rotation Angle
fig, ax1 = plt.subplots(figsize=(8, 4.5), dpi=300)

ax1.plot(df['rotation_deg'], df['Fx'], label=r'$F_x$ (Radial Push)', color='#1f77b4', linewidth=1.5)
ax1.plot(df['rotation_deg'], df['Fy'], label=r'$F_y$ (Transverse Push)', color='#ff7f0e', linewidth=1.5)
ax1.plot(df['rotation_deg'], df['Fz'], label=r'$F_z$ (Out-of-Plane Push)', color='#2ca02c', linewidth=1.5)

ax1.set_xlabel('Asteroid Rotation Angle (Degrees)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Net Force Vector Components (N)', fontsize=11, fontweight='bold')
ax1.set_title('Bennu Net Solar Radiation Pressure Forces Over 360° Rotation', fontsize=12, pad=12, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(loc='upper right', frameon=True)
plt.tight_layout()
plt.savefig("bennu_force_components.png", dpi=300)
plt.close()

# Figure 2: YORP Torques (Tau_X, Tau_Y, Tau_Z) vs. Rotation Angle
fig, ax2 = plt.subplots(figsize=(8, 4.5), dpi=300)

ax2.plot(df['rotation_deg'], df['Tau_x'], label=r'$\tau_x$', color='#d62728', linestyle='--', alpha=0.7)
ax2.plot(df['rotation_deg'], df['Tau_y'], label=r'$\tau_y$', color='#9467bd', linestyle='--', alpha=0.7)
ax2.plot(df['rotation_deg'], df['Tau_z'], label=r'$\tau_z$ (Primary Spin Axis)', color='#17becf', linewidth=2.0)

# Add horizontal zero reference line
ax2.axhline(0, color='black', linestyle=':', linewidth=1.0)

ax2.set_xlabel('Asteroid Rotation Angle (Degrees)', fontsize=11, fontweight='bold')
ax2.set_ylabel(r'Net YORP Torque Vector ($\mathrm{N \cdot m}$)', fontsize=11, fontweight='bold')
ax2.set_title('Bennu Net YORP Torque Profiles Over 360° Rotation', fontsize=12, pad=12, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(loc='upper right', frameon=True)
plt.tight_layout()
plt.savefig("bennu_torque_profiles.png", dpi=300)
plt.close()

# Summary Output Statistics
mean_tau_z = df['Tau_z'].mean()
print("=== Publication Visualizations Generated ===")
print("Saved figures: 'bennu_force_components.png' and 'bennu_torque_profiles.png'")
print(f"Mean Daily Tau_Z Torque : {mean_tau_z:.6e} N·m")