import numpy as np
import matplotlib.pyplot as plt

# 1. Загрузка данных из py21.txt
py_data = np.loadtxt('py21.txt', skiprows=1)  # Пропускаем заголовок
theta_py_rad = py_data[:, 0]
d_py_lin = py_data[:, 1]
d_py_db = py_data[:, 2]

# 2. Загрузка данных из newcst.txt
with open('newcst.txt', 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

# Первая половина — линейные данные
cst_lin_lines = lines[:361]
cst_db_lines = lines[361:722]  # следующие 361 строки

def parse_cst_block(block):
    thetas = []
    vals = []
    for line in block:
        parts = line.replace(',', '.').split()
        if len(parts) < 3:
            continue
        theta_deg = float(parts[1])
        val = float(parts[2])
        thetas.append(np.deg2rad(theta_deg))
        vals.append(val)
    return np.array(thetas), np.array(vals)

theta_cst_rad, d_cst_lin = parse_cst_block(cst_lin_lines)
_, d_cst_db = parse_cst_block(cst_db_lines)

# 3. Фильтрация данных: оставляем только 0–180 градусов (0–π рад)
# Предполагаем, что угол идёт от 0 до 360 градусов → 0–2π рад
mask_py = (theta_py_rad >= 0) & (theta_py_rad <= np.pi)
mask_cst = (theta_cst_rad >= 0) & (theta_cst_rad <= np.pi)

theta_py_180 = theta_py_rad[mask_py]
d_py_lin_180 = d_py_lin[mask_py]
d_py_db_180 = d_py_db[mask_py]

theta_cst_180 = theta_cst_rad[mask_cst]
d_cst_lin_180 = d_cst_lin[mask_cst]
d_cst_db_180 = d_cst_db[mask_cst]

# 4. Графики
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# --- Декартова система: линейная ДН (0–180°) ---
axs[0, 0].plot(np.rad2deg(theta_py_180), d_py_lin_180, label='Python', color='blue')
axs[0, 0].plot(np.rad2deg(theta_cst_180), d_cst_lin_180, label='CST', color='orange', linestyle='--')
axs[0, 0].set_xlabel('Theta (градусы)')
axs[0, 0].set_ylabel('ДН (разы)')
axs[0, 0].set_title('Декарт: ДН (разы), 0–180°')
axs[0, 0].legend()
axs[0, 0].grid(True)
axs[0, 0].set_xlim(0, 180)

# --- Декартова система: ДН в дБ (0–180°) ---
axs[0, 1].plot(np.rad2deg(theta_py_180), d_py_db_180, label='Python', color='blue')
axs[0, 1].plot(np.rad2deg(theta_cst_180), d_cst_db_180, label='CST', color='orange', linestyle='--')
axs[0, 1].set_xlabel('Theta (градусы)')
axs[0, 1].set_ylabel('ДН (дБ)')
axs[0, 1].set_title('Декарт: ДН (дБ), 0–180°')
axs[0, 1].legend()
axs[0, 1].grid(True)
axs[0, 1].set_xlim(0, 180)

# --- Полярная система: линейная ДН (0–π) ---
ax_polar_lin = plt.subplot(2, 2, 3, projection='polar')
ax_polar_lin.plot(theta_py_180, d_py_lin_180, label='Python', color='blue')
ax_polar_lin.plot(theta_cst_180, d_cst_lin_180, label='CST', color='orange', linestyle='--')
ax_polar_lin.set_title('Полярная: ДН (разы), 0–180°')
ax_polar_lin.set_thetamin(0)
ax_polar_lin.set_thetamax(180)
ax_polar_lin.legend(loc='upper right')

# --- Полярная система: ДН в дБ (0–π) ---
ax_polar_db = plt.subplot(2, 2, 4, projection='polar')
ax_polar_db.plot(theta_py_180, d_py_db_180, label='Python', color='blue')
ax_polar_db.plot(theta_cst_180, d_cst_db_180, label='CST', color='orange', linestyle='--')
ax_polar_db.set_title('Полярная: ДН (дБ), 0–180°')
ax_polar_db.set_thetamin(0)
ax_polar_db.set_thetamax(180)
ax_polar_db.legend(loc='upper right')

plt.tight_layout()
plt.show()