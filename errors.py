import numpy as np
import sympy as sp


class UnKnownOperator(Exception):
    pass


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


def convert_unit_to_latex(unit: str) -> str:
    known_operators = ["/", "*", "^"]
    unit = unit.replace(" ", "")
    latex = ""
    for i, character in enumerate(unit):
        if character == "/":
            return f"\\frac{{{unit[:i]}}}{{{convert_unit_to_latex(unit[i + 1:])}}}"
        elif character == "*":
            return f"{unit[:i]}\cdot{convert_unit_to_latex(unit[i + 1:])}"
        elif character == "^":
            return f"{unit[:i]} ^ {{{unit[i + 1]}}} {convert_unit_to_latex(unit[i + 2:])}"
        elif not character.isalpha():
            raise UnKnownOperator(
                f"You passed unknown operator{character}, please make sure it is one of these {known_operators}")
    return unit


def calculate_stats_with_delta(numbers: list[int | float], var_name: str, delta_m: int | float, unit: str) -> str:
    unit = convert_unit_to_latex(unit)

    numbers = np.array(numbers)
    n = len(numbers)

    mean = format_float(np.mean(numbers))

    std_dev = format_float(np.sqrt(np.sum((numbers - mean) ** 2) / (n - 1)))

    delta_s = format_float(std_dev / np.sqrt(n))

    delta = format_float(np.sqrt(delta_m ** 2 + delta_s ** 2))
    latex_numbers = ""
    for i in range(len(numbers)):
        latex_numbers += (
            f"\\{var_name}_{i} = {numbers[i]}[{unit}] "
        )
    latex_numbers += "\n"

    latex_mean = (
        f"\\bar{{{var_name}}} = "
        f"\\frac{{1}}{{n}} \\sum_{{i=1}}^{{n}} {var_name}_i = {mean}"
        "\n"
        f"\\boxed{{\\bar{{{var_name}}} = {mean}[{unit}]}}"
        "\n"
    )
    latex_std = (
        f"\\sigma = "
        f"\\sqrt{{\\frac{{1}}{{n-1}} \\sum_{{i=1}}^{{n}} ({var_name}_i - \\bar{{{var_name}}})^2}}"
        "\n"
        f"\\boxed{{\\sigma = {std_dev}[{unit}]}}"
        "\n"
    )
    latex_delta_s = (
        f"\\Delta {var_name}_s = \\frac{{\\sigma}}{{\\sqrt{{n}}}} = "
        f"\\frac{{{std_dev}}}{{\\sqrt{{{n}}}}}"
        "\n"
        f"\\Delta {var_name}_s = {delta_s}[{unit}]"
        "\n"
    )
    latex_delta = (
        f"\\Delta {var_name} = \\sqrt{{\\Delta {var_name}_m^{{2}} + \\Delta {var_name}_S^{{2}}}} = "
        f"\\sqrt{{{delta_m}^{{2}} + {delta_s}^{{2}}}}"
        "\n"
        f"\\boxed{{\\Delta {var_name} = {delta}[{unit}]}}"
    )
    latex = latex_numbers + latex_mean + latex_std + latex_delta_s + latex_delta
    return latex


def calculate_error_with_propagation(formula: str,
                                     calculated_variable: str,
                                     variables: dict[str, float | int],
                                     errors: dict[str, float | int],
                                     unit: str = "s") -> tuple[float, float, str]:
    unit = convert_unit_to_latex(unit)
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
            r"\Delta " + calculated_variable + r"_{" + f"{var}" + r"} = \frac{{\partial " + calculated_variable + "}}{{\partial " + f"{var}" + r"}} \Delta " + f"{calculated_variable}_" + f"{var} = " +
            f"({sp.latex(partial_derivative)}) \\cdot {error}"
            "\n"
            f"\\Delta {calculated_variable}_{{{var}}} = {delta_term}[{unit}]"
            "\n"
        )

    delta_result = format_float(sum(error_terms) ** 0.5)

    error_sum_latex = " + ".join(
        [r"\Delta " + calculated_variable + "_{" + f"{var}" + r"}^{2}" for var in errors.keys()])
    latex = (
            "\\boxed{" + calculated_variable + r" = " + f"{sp.latex(formula_expr)} = {formula_value}[{unit}]}}\n\n" +
            "\n\n".join(latex_terms) +
            r"\n\n\Delta " + calculated_variable + " = \sqrt{" + error_sum_latex + "}"
                                                                                   "\n"
                                                                                   f"\\boxed{{\Delta {calculated_variable} = {delta_result}[{unit}]}}"
                                                                                   "\n"
    )
    return float(formula_value), float(delta_result), latex


def calculate_n_sigma(theoretical_result: float | int,
                      experiment_result: float | int,
                      theoretical_error: float | int,
                      experiment_error: float | int,
                      calculated_variable: str) -> tuple[float, float, str]:
    delta_k = format_float(abs(experiment_result - theoretical_result) / theoretical_result)
    n_sigma = format_float(abs(theoretical_result - experiment_result) / ((theoretical_error ** 2 + experiment_error ** 2) ** 0.5))
    latex_delta_k = (
        f"\\Delta K = \\frac{{\\left|K_{{\\text{{exp}}}} - K_{{\\text{{th}}}}\\right|}}{{K_{{\\text{{th}}}}}}"
        "\n\n"
        f"\\Delta K = \\frac{{\\left|{experiment_result} - {theoretical_result}\\right|}}{{{theoretical_result}}}"
        "\n\n"
        f"\\Delta K = {delta_k}"
        "\n\n"
    )
    latex_n_sigma = (
        f"N_\\sigma = \\frac{{\\left|{calculated_variable}_{{\\text{{th}}}} - {calculated_variable}_{{\\text{{exp}}}}\\right|}}{{\\sqrt{{\\Delta {calculated_variable}_{{\\text{{th}}}} ^ {2} + \\Delta {calculated_variable}_{{\\text{{exp}}}} ^ {2} }}}}"
        "\n\n"
        f"N_\\sigma = \\frac{{\\left|{theoretical_result} - {experiment_result}\\right|}}{{\\sqrt{{{theoretical_error} ^ {2} + {experiment_error} ^ {2}}}}}"
        "\n\n"
        f"\\boxed{{N_\\sigma = {n_sigma}}}"
    )
    latex = latex_delta_k + latex_n_sigma
    return delta_k, n_sigma, latex


print(calculate_n_sigma(1.0268,1.0053,0.0011,0.009,"T"))
