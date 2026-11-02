"""Количество натуральных делителей: O(sqrt(X)), X <= 2_000_000_000."""

from math import isqrt


def divisor_count(x):
    if x < 1:
        raise ValueError("X должно быть натуральным")
    result = 0
    for divisor in range(1, isqrt(x) + 1):
        if x % divisor == 0:
            result += 1 if divisor * divisor == x else 2
    return result


def main():
    print(divisor_count(int(input())))


if __name__ == "__main__":
    main()
