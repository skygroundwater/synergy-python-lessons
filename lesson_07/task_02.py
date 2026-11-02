"""Замена каждой группы последовательных пробелов одним пробелом."""


def compress_spaces(text):
    while "  " in text:
        text = text.replace("  ", " ")
    return text


def main():
    print(compress_spaces(input()))


if __name__ == "__main__":
    main()
