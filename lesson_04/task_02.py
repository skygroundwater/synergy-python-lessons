"""Вычисление выражения из цифр пятизначного числа."""


def calculate(number):
    number = abs(number)
    if not 10000 <= number <= 99999:
        raise ValueError("Требуется пятизначное целое число")
    units = number % 10
    tens = number // 10 % 10
    hundreds = number // 100 % 10
    thousands = number // 1000 % 10
    ten_thousands = number // 10000
    denominator = ten_thousands - thousands
    if denominator == 0:
        raise ZeroDivisionError("Разность десятков тысяч и тысяч равна нулю")
    return (tens ** units) * hundreds / denominator


def main():
    try:
        print(calculate(int(input("Пятизначное число: "))))
    except (ValueError, ZeroDivisionError) as error:
        print("Ошибка:", error)


if __name__ == "__main__":
    main()
