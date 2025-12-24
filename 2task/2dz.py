import numpy as np
import matplotlib.pyplot as plt

def E(theta):
    num = np.cos(k * l * np.cos(theta)) - np.cos(k * l)
    den = np.sin(theta)
    return num / den

def F(theta):
    return np.abs(E(theta)) / np.abs(E(theta)).max()

def Dmax(theta):
    formula = (F(theta)**2) * np.sin(theta)
    integral = np.trapezoid(formula, theta)
    return 2 / integral

def D(theta):
    return (F(theta)**2) * Dmax(theta)

def creating_plot(d_times, d_dB, theta):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('D(Theta)')

    # Декартовы графики
    axs[0, 0].plot(theta, d_times, color='blue')
    axs[0, 0].set_title("КНД (разы, декарт)")
    axs[0, 0].set_xlabel("θ (рад)")
    axs[0, 0].set_ylabel("D(θ)")
    axs[0, 0].grid(True)

    axs[0, 1].plot(theta, d_dB, color='red')
    axs[0, 1].set_title("КНД (дБ, декарт)")
    axs[0, 1].set_xlabel("θ (рад)")
    axs[0, 1].set_ylabel("D(θ) [дБ]")
    axs[0, 1].grid(True)

    # Полярные графики
    ax_polar1 = plt.subplot(2, 2, 3, polar=True)
    ax_polar1.plot(theta, d_times, color='blue')
    ax_polar1.set_title("КНД (разы, поляр)")

    ax_polar2 = plt.subplot(2, 2, 4, polar=True)
    ax_polar2.plot(theta, d_dB, color='red')
    ax_polar2.set_title("КНД (дБ, поляр)")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('task2var1.png')
    plt.show()

def main():
    global l, k
    f = 0.1e9
    c = 3e8
    lmbd = c / f
    l = lmbd / 2
    k = 2 * np.pi / lmbd
    theta = np.linspace(1e-9, np.pi - 1e-9, 2000)

    d_times = D(theta)
    d_dB = 10 * np.log10(d_times + 1e-9)  # избегаем log(0)

    dmax_val = Dmax(theta)
    print(f'{dmax_val:.3f} times')
    print(f'{10 * np.log10(dmax_val):.3f} dB')

    creating_plot(d_times=d_times, d_dB=d_dB, theta=theta)

    with open('py21.txt', 'w', encoding='utf-8') as file:
        file.write('theta   d_times   d_db\n')
        for i in range(len(theta)):
            file.write(f'{theta[i]:.6f}   {d_times[i]:.6f}   {d_dB[i]:.6f}\n')

if __name__ == "__main__":
    main()

