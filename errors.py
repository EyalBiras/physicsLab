import numpy as np
import sympy as sp

def get_distance_to_zero(num: float) -> int:
    if num == 0:
        return 0
    if num > 1:
        return 0
    distance = 0
    while abs(num) < 1:
        num *= 10
        distance += 1
    return distance

def format_float(num: float | np.floating, significant_digits: int = 1) -> float:
    int_part = int(num)
    float_part = num - int_part
    return int_part + round(float_part, get_distance_to_zero(float_part) + significant_digits)



def calculate_stats_with_delta(numbers: list[int | float], var_name: str, delta_m: int | float) -> str:
    numbers = np.array(numbers)
    n = len(numbers)

    mean = format_float(np.mean(numbers))

    std_dev = format_float(np.sqrt(np.sum((numbers - mean) ** 2) / (n - 1)))

    delta_s = format_float(std_dev / np.sqrt(n))

    delta = format_float(np.sqrt(delta_m ** 2 + delta_s ** 2))

    latex_mean = (
        f"\\bar{{{var_name}}} = "
        f"\\frac{{1}}{{n}} \\sum_{{i=1}}^{{n}} {var_name}_i = {mean}"
        "\n"
    )
    latex_std = (
        f"\\sigma = "
        f"\\sqrt{{\\frac{{1}}{{n-1}} \\sum_{{i=1}}^{{n}} ({var_name}_i - \\bar{{{var_name}}})^2}} = {std_dev}"
        "\n"
    )
    latex_delta_s = (
        f"\\Delta {var_name}_s = \\frac{{\\sigma}}{{\\sqrt{{n}}}} = "
        f"\\frac{{{std_dev}}}{{\\sqrt{{{n}}}}} = {delta_s}"
        "\n"
    )
    latex_delta = (
        f"\\Delta {var_name} = \\sqrt{{\\Delta {var_name}_m^{{2}} + \\Delta {var_name}_S^{{2}}}} = "
        f"\\sqrt{{{delta_m}^{{2}} + {delta_s}^{{2}}}} = {delta}"
        "\n"
    )
    latex = latex_mean + latex_std + latex_delta_s + latex_delta

    return latex


def calculate_error_with_propagation(formula: str, calculated_variable: str, variables: dict[str, float | int],
                                     errors: dict[str, float | int]) -> tuple[float, float, str]:
    symbols = {name: sp.symbols(name) for name in variables.keys()}

    formula_expr = sp.sympify(formula)

    formula_value = format_float(formula_expr.evalf(subs=variables))

    error_terms = []
    latex_terms = []
    for var, error in errors.items():
        error = format_float(error)
        partial_derivative = sp.diff(formula_expr, symbols[var])
        partial_value = partial_derivative.evalf(subs=variables)
        delta_term = format_float(partial_value * error)
        error_terms.append(format_float(delta_term ** 2))

        latex_terms.append(
            r"\Delta " + calculated_variable + r"_{" + f"{var}" + r"} = \frac{{\partial "+ calculated_variable +"}}{{\partial " + f"{var}" + r"}} \Delta " + f"{var} = " +
            f"({sp.latex(partial_derivative)}) \\cdot {error} = {delta_term}"
        )

    delta_result = format_float(sum(error_terms) ** 0.5)

    error_sum_latex = " + ".join(
        [r"\Delta " + calculated_variable + "_{" + f"{var}" + r"}^{2}" for var in errors.keys()])
    latex = (
            calculated_variable +r" = " + f"{sp.latex(formula_expr)} = {formula_value}\n\n" +
            "\n\n".join(latex_terms) +
            r"\n\n\Delta " + calculated_variable + " = \sqrt{" + error_sum_latex + "} = " + f"{delta_result}"
    )

    return float(formula_value), float(delta_result), latex


