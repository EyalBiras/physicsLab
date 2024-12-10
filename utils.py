import numpy as np


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

def convert_mul_div_latex(unit: str) -> str:
    known_operators = ["/", "*", ]
    unit = unit.replace(" ", "")
    latex = ""
    for i, character in enumerate(unit):
        if character == "/":
            return f"\\frac{{{unit[:i]}}}{{{convert_unit_to_latex(unit[i + 1:])}}}"
        elif character == "*":
            return f"{unit[:i]}\cdot{convert_unit_to_latex(unit[i + 1:])}"
        elif character == "^":
            pass
        elif not character.isalpha() and not character.isdigit():
            raise UnKnownOperator(
                f"You passed unknown operator{character}, please make sure it is one of these {known_operators}")
    return unit


def convert_unit_to_latex(unit: str) -> str:
    known_latex_operators = ["/", "*", "^", "\\", "{", "}"]
    unit = unit.replace(" ", "")
    unit = convert_mul_div_latex(unit)
    latex = ""
    for i, character in enumerate(unit):
        if character == "^":
            latex += "^"
        elif unit[i - 1] == "^":
            latex += f"{{{unit[i]}}}"
        elif not character.isalpha() and not character.isdigit() and character not in known_latex_operators:
            raise UnKnownOperator(
                f"You passed unknown operator{character}, please make sure it is one of these {known_operators}")
        else:
            latex += character
    return unit


