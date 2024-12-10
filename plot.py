import matplotlib.pyplot as plt
import numpy as np

from errors import calculate_stats_with_delta
from utils import convert_unit_to_latex


def plot_with_error_bars(x: list[int | float],
                         y: list[int | float],
                         x_errors: list[int | float],
                         y_errors: list[int | float],
                         x_label: str = "X-axis",
                         y_label: str = "Y-axis",
                         x_unit: str = "",
                         y_unit: str = "",
                         amount_of_ticks: int = 10,
                         plot_title: str = "Plot with Error Bars"):
    plt.rcParams.update({
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 15
    })
    x = np.array(x)
    y = np.array(y)
    x_unit = convert_unit_to_latex(x_unit)
    y_unit = convert_unit_to_latex(y_unit)
    x_label_full = f"${x_label} \\, [{x_unit}]$" if x_unit else f"${x_label}$"
    y_label_full = f"${y_label} \\, [{y_unit}]$" if y_unit else f"${y_label}$"
    m, b = np.polyfit(x, y, 1)
    trend_line = m * x + b

    plt.plot(x, trend_line, color='red', label=f'trend line (y = {m:.2f}x + {b:.2f})')

    plt.errorbar(x, y, xerr=x_errors, yerr=y_errors, fmt='o', capsize=5, label="Data with errors")
    plt.title(f"${plot_title}$", fontsize=30)
    plt.xlabel(x_label_full, fontsize=20)
    plt.ylabel(y_label_full, fontsize=20)
    plt.legend()
    plt.grid()
    plt.locator_params(axis="x", nbins=len(x) * amount_of_ticks)
    plt.locator_params(axis="y", nbins=len(y) * amount_of_ticks)
    plt.show()



