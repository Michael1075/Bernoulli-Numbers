# import numpy as np
# from scipy.special import comb
from fractions import Fraction
import re
import time


def get_pascal_triangle_layer(n):
    # return comb(np.full(n + 1, n), np.arange(n + 1)).astype(np.int)
    c = 1
    result = [1]
    for k in range(n):
        c = c * (n - k) // (k + 1)
        result.append(c)
    return result


def generate_bernuoulli_numbers(n):
    result = [Fraction(1)]
    for k in range(2, n + 1):
        # result.append(-np.sum(get_pascal_triangle_layer(k)[:-2] * result) / k)
        temp_sum = Fraction()
        for c, r in zip(get_pascal_triangle_layer(k)[:-2], result):
            temp_sum += c * r
        result.append(-temp_sum / k)
    return result


def get_polynomial_coefficients(n):
    result = []
    sign = 1
    for c, b in zip(get_pascal_triangle_layer(n)[:-1], generate_bernuoulli_numbers(n)):
        result.append(sign * c * b / n)
        sign *= -1
    result.append(Fraction())
    return result


def calculate_polynomial_result(coefficients, x):
    result = 0
    power = 1
    for coefficient in reversed(coefficients):
        result += coefficient * power
        power *= x
    return result


def calculate_power_sum(p, n):
    return calculate_polynomial_result(get_polynomial_coefficients(p + 1), n)


def original_power_sum(p, n):
    return sum([i ** p for i in range(n + 1)])


def get_polynomial_str(coefficients, var="x"):
    parts = []
    exponent = len(coefficients)
    for coefficient in coefficients:
        exponent -= 1
        if not coefficient:
            continue
        if coefficient > 0:
            parts.append(f"+ {coefficient} * {var}^{exponent}")
        else:
            parts.append(f"- {-coefficient} * {var}^{exponent}")
    result = " ".join(parts)
    if not result:
        return "0"
    if result.startswith("+"):
        return result[2:]
    else:
        return "-" + result[2:]


def write_bernoulli_polynomial(n, var="x"):
    return get_polynomial_str(get_polynomial_coefficients(n), var)


def parse_range(number_or_range_str):
    if ":" not in number_or_range_str:
        number = int(number_or_range_str)
        return range(number, number + 1)
    left, right = number_or_range_str.split(":")
    left = 0 if not left else int(left)
    right = int(right)
    return range(left, right)


def time_decorator(func):
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print("Running time: {0:.6f} second(s)".format(end_time - begin_time))
    return wrapper


@time_decorator
def calculate_sum_mode(p_range, n_range):
    for p in p_range:
        coefficients = get_polynomial_coefficients(p + 1)
        for n in n_range:
            result = calculate_polynomial_result(coefficients, n)
            print(f"S^{p}({n}) = {result}")


@time_decorator
def formula_mode(p_range):
    for p in p_range:
        result = write_bernoulli_polynomial(p + 1, "n")
        print(f"S^{p}(n) = {result}")


@time_decorator
def bernoulli_numbers_mode(n_range):
    result = generate_bernuoulli_numbers(n_range.stop)
    for n in n_range:
        print(f"B_{n} = {result[n]}")


def parse_cmd(cmd_str):
    num_or_range_pattern = r"(\:?\d+|\d+\:\d+)"
    calculate_sum_pattern = r"^S\^A\(A\)$".replace("A", num_or_range_pattern)
    formula_pattern = r"^S\^A\(n\)$".replace("A", num_or_range_pattern)
    bernoulli_numbers_pattern = r"^B_A$".replace("A", num_or_range_pattern)
    range_warning_msg = "Something's wrong with the command's range."
    
    match_obj = re.match(calculate_sum_pattern, cmd_str)
    if match_obj:
        p_range = parse_range(match_obj.group(1))
        n_range = parse_range(match_obj.group(2))
        if not (p_range and n_range):
            print(range_warning_msg)
            return
        calculate_sum_mode(p_range, n_range)
        return

    match_obj = re.match(formula_pattern, cmd_str)
    if match_obj:
        p_range = parse_range(match_obj.group(1))
        if not (p_range):
            print(range_warning_msg)
        formula_mode(p_range)
        return

    match_obj = re.match(bernoulli_numbers_pattern, cmd_str)
    if match_obj:
        n_range = parse_range(match_obj.group(1))
        if not (n_range):
            print(range_warning_msg)
        bernoulli_numbers_mode(n_range)
        return
    
    print("Please check your command.")


if __name__ == "__main__":
    while True:
        cmd_str = input()
        if cmd_str == "q":
            break
        parse_cmd(cmd_str)
        print()
