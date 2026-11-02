"""Факториал числа и список факториалов от n! до 1 в обратном порядке."""


def factorial(number):
    if not isinstance(number, int) or number < 0:
        raise ValueError("Требуется неотрицательное целое число")
    result = 1
    for value in range(2, number + 1):
        result *= value
    return result


def factorials_from_factorial(number):
    maximum = factorial(number)
    values = []
    current = 1
    for value in range(1, maximum + 1):
        current *= value
        values.append(current)
    values.reverse()
    return values


def main():
    number = int(input())
    print("Факториал:", factorial(number))
    print(factorials_from_factorial(number))


if __name__ == "__main__":
    main()
