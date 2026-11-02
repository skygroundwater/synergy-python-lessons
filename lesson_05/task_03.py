"""Определение возможности инвестировать по порогу X."""


def investors(x, a, b):
    if a >= x and b >= x:
        return "2"
    if a >= x:
        return "Mike"
    if b >= x:
        return "Ivan"
    if a + b >= x:
        return "1"
    return "0"


def main():
    x = int(input())
    a = int(input())
    b = int(input())
    print(investors(x, a, b))


if __name__ == "__main__":
    main()
