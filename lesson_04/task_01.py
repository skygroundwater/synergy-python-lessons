"""Площадь и периметр прямоугольника с вещественными сторонами."""


def rectangle(a, b):
    if a <= 0 or b <= 0:
        raise ValueError("Стороны прямоугольника должны быть положительными")
    return a * b, 2 * (a + b)


def main():
    a = float(input("Первая сторона: "))
    b = float(input("Вторая сторона: "))
    area, perimeter = rectangle(a, b)
    print("Площадь:", area)
    print("Периметр:", perimeter)


if __name__ == "__main__":
    main()
