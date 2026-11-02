"""Описание знака и чётности целого числа."""


def describe(number):
    if number == 0:
        return "нулевое число"
    sign = "положительное" if number > 0 else "отрицательное"
    parity = "четное" if number % 2 == 0 else "нечетное"
    return f"{sign} {parity} число"


def main():
    number = int(input())
    print(describe(number))
    # Дополнительное сообщение для нечётного числа прямо требуется в условии.
    if number % 2 != 0:
        print("число не является четным")


if __name__ == "__main__":
    main()
