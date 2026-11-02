"""Циклический сдвиг списка вправо на один элемент, с изменением списка."""


def rotate_right(numbers):
    if numbers:
        numbers.insert(0, numbers.pop())


def main():
    n = int(input())
    numbers = list(map(int, input().split()))
    if len(numbers) != n:
        raise ValueError("Количество чисел не совпадает с N")
    rotate_right(numbers)
    print(*numbers)


if __name__ == "__main__":
    main()
