import numpy as np
import xml.etree.ElementTree as ET
from scipy.special import spherical_jn, spherical_yn
import csv


class RCSCalculator:
    """Класс для расчёта ЭПР идеально проводящей сферы."""

    def __init__(self, diameter):
        self.r = diameter / 2.0  # радиус сферы
        self.c = 3e8  # скорость света

    def spherical_hn1(self, n, x):
        """Сферическая функция Бесселя 3-го рода (Ханкеля) 1-го вида."""
        return spherical_jn(n, x) + 1j * spherical_yn(n, x)

    def calculate_rcs(self, freq):
        """Рассчитывает ЭПР для заданной частоты."""
        k = 2 * np.pi * freq / self.c  # волновое число
        lam = self.c / freq  # длина волны
        kr = k * self.r

        if kr == 0:
            return 0.0

        # Рассчитываем сумму ряда
        sum_term = 0j
        n = 1
        max_n = int(10 + np.abs(kr) * 1.5)  # эмпирическое правило для сходимости

        while n <= max_n:
            jn_kr = spherical_jn(n, kr)
            yn_kr = spherical_yn(n, kr)
            hn_kr = self.spherical_hn1(n, kr)

            # Коэффициенты a_n и b_n
            a_n = spherical_jn(n, kr) / hn_kr

            # Для b_n нужны функции от n-1
            jn1_kr = spherical_jn(n - 1, kr) if n >= 1 else spherical_jn(0, kr)
            hn1_kr = self.spherical_hn1(n - 1, kr) if n >= 1 else self.spherical_hn1(0, kr)

            numerator = kr * jn1_kr - n * jn_kr
            denominator = kr * hn1_kr - n * hn_kr
            b_n = numerator / denominator

            term = (-1) ** n * (n + 0.5) * (b_n - a_n)
            sum_term += term

            # Проверка сходимости
            if n > 5 and np.abs(term) < 1e-6 * np.abs(sum_term):
                break

            n += 1

        # Формула ЭПР
        rcs = (lam ** 2 / np.pi) * np.abs(sum_term) ** 2
        return float(np.real(rcs))  # возвращаем вещественную часть


class ResultWriter:
    """Класс для записи результатов в различных форматах."""

    def __init__(self, format_type):
        self.format_type = format_type

    def write(self, data, filename):
        """Записывает данные в файл в указанном формате."""
        if self.format_type == 1:  # TXT
            self._write_txt(data, filename)
        elif self.format_type == 2:  # CSV
            self._write_csv(data, filename)
        else:
            raise ValueError(f"Неизвестный формат: {self.format_type}")

    def _write_txt(self, data, filename):
        """Запись в текстовый формат (столбцы разделены 4 пробелами)."""
        with open(filename, 'w') as f:
            for freq, rcs in data:
                f.write(f"{freq:.6e}    {rcs:.6e}\n")

    def _write_csv(self, data, filename):
        """Запись в CSV формат (номер строки, частота, ЭПР)."""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['No', 'Frequency (Hz)', 'RCS (m^2)'])
            for i, (freq, rcs) in enumerate(data, 1):
                writer.writerow([i, f"{freq:.6e}", f"{rcs:.6e}"])


def read_parameters_from_xml(xml_file, variant_number):
    """Чтение параметров из XML файла для заданного варианта."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Поиск варианта по номеру (для варианта 21 берем variant number="2")
    variant = root.find(f"./variant[@number='{variant_number}']")

    if variant is None:
        raise ValueError(f"Вариант {variant_number} не найден в файле {xml_file}")

    D = float(variant.find('D').text)
    fmin = float(variant.find('fmin').text)
    fmax = float(variant.find('fmax').text)

    return D, fmin, fmax


def main():
    # Параметры для варианта 21
    xml_file = "task_rcs_02.xml"
    variant_number = 2  # Для варианта 21 из таблицы (21-25 соответствуют 1-5 в файле)
    output_format = 2  # CSV формат

    # Чтение параметров
    D, fmin, fmax = read_parameters_from_xml(xml_file, variant_number)

    print(f"Диаметр сферы: {D} м")
    print(f"Диапазон частот: от {fmin:.2e} Гц до {fmax:.2e} Гц")

    # Создание калькулятора
    calculator = RCSCalculator(D)

    # Генерация частот (логарифмическая шкала для лучшего отображения)
    num_points = 1000
    freqs = np.logspace(np.log10(fmin), np.log10(fmax), num_points)

    # Расчет ЭПР для каждой частоты
    results = []
    for freq in freqs:
        rcs = calculator.calculate_rcs(freq)
        results.append((freq, rcs))
        if len(results) <= 5:  # Вывод первых 5 значений для проверки
            print(f"f = {freq:.2e} Гц, ЭПР = {rcs:.6e} м²")

    # Создание графика
    import matplotlib.pyplot as plt

    plt.plot(freqs, [r[1] for r in results], 'b-', linewidth=2)
    plt.xlabel('Частота (Гц)', fontsize=12)
    plt.ylabel('ЭПР (м²)', fontsize=12)
    plt.title(f'ЭПР идеально проводящей сферы (D={D} м)', fontsize=14)
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.savefig('rcs_vs_frequency.png', dpi=300)
    plt.show()

    # Запись результатов
    writer = ResultWriter(output_format)
    output_file = "result_rcs.csv"
    writer.write(results, output_file)
    print(f"\nРезультаты сохранены в файл: {output_file}")

    # Вывод первых 20 строк результата
    print("\nПервые 20 строк результата:")
    print("=" * 50)
    print("No\tFrequency (Hz)\t\tRCS (m^2)")
    print("-" * 50)
    for i, (freq, rcs) in enumerate(results[:20], 1):
        print(f"{i}\t{freq:.6e}\t{rcs:.6e}")


if __name__ == "__main__":
    main()


