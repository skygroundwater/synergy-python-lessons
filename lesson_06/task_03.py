"""Все чётные числа от A до B включительно."""


def main():
    a = int(input())
    b = int(input())
    first_even = a if a % 2 == 0 else a + 1
    print(*range(first_even, b + 1, 2))


if __name__ == "__main__":
    main()
