"""Разворот списка из N чисел."""


def main():
    n = int(input())
    numbers = [int(input()) for _ in range(n)]
    numbers.reverse()
    print(*numbers)


if __name__ == "__main__":
    main()
