"""Количество различных чисел в последовательности."""


def main():
    n = int(input())
    numbers = list(map(int, input().split()))
    if len(numbers) != n:
        raise ValueError("Количество чисел не совпадает с N")
    print(len(set(numbers)))


if __name__ == "__main__":
    main()
