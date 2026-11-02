"""Количество различных чисел, общих для двух списков."""


def main():
    first = set(map(int, input().split()))
    second = set(map(int, input().split()))
    print(len(first & second))


if __name__ == "__main__":
    main()
