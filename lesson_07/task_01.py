"""Проверка строки на палиндром."""


def is_palindrome(text):
    return text == text[::-1]


def main():
    print("yes" if is_palindrome(input()) else "no")


if __name__ == "__main__":
    main()
