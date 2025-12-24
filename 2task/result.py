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

# Убедимся, что углы совпадают (они идут от 0 до 360 градусов → 0–2π рад)
# Для корректного отображения в полярных графиках:
theta_full = theta_cst_rad  # 0 → 2π

# 3. Графики
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# --- Декартова система: линейная ДН ---
axs[0, 0].plot(np.rad2deg(theta_py_rad), d_py_lin, label='Python', color='blue')
axs[0, 0].plot(np.rad2deg(theta_full), d_cst_lin, label='CST', color='orange', linestyle='--')
axs[0, 0].set_xlabel('Theta (градусы)')
axs[0, 0].set_ylabel('ДН (разы)')
axs[0, 0].set_title('Декарт: ДН (разы)')
axs[0, 0].legend()
axs[0, 0].grid(True)

# --- Декартова система: ДН в дБ ---
axs[0, 1].plot(np.rad2deg(theta_py_rad), d_py_db, label='Python', color='blue')
axs[0, 1].plot(np.rad2deg(theta_full), d_cst_db, label='CST', color='orange', linestyle='--')
axs[0, 1].set_xlabel('Theta (градусы)')
axs[0, 1].set_ylabel('ДН (дБ)')
axs[0, 1].set_title('Декарт: ДН (дБ)')
axs[0, 1].legend()
axs[0, 1].grid(True)

# --- Полярная система: линейная ДН ---
ax_polar_lin = plt.subplot(2, 2, 3, projection='polar')
ax_polar_lin.plot(theta_py_rad, d_py_lin, label='Python', color='blue')
ax_polar_lin.plot(theta_full, d_cst_lin, label='CST', color='orange', linestyle='--')
ax_polar_lin.set_title('Полярная: ДН (разы)')
ax_polar_lin.legend(loc='upper right')

# --- Полярная система: ДН в дБ ---
# Чтобы избежать проблем с отрицательными/нулевыми значениями, можно использовать линейную амплитуду
# Но если хочется именно дБ — тогда просто отображаем как есть (может быть отрицательно)
ax_polar_db = plt.subplot(2, 2, 4, projection='polar')
ax_polar_db.plot(theta_py_rad, d_py_db, label='Python', color='blue')
ax_polar_db.plot(theta_full, d_cst_db, label='CST', color='orange', linestyle='--')
ax_polar_db.set_title('Полярная: ДН (дБ)')
ax_polar_db.legend(loc='upper right')

plt.tight_layout()
plt.show()