"""YES для уже встречавшегося числа, иначе NO."""


def main():
    seen = set()
    for number in map(int, input().split()):
        print("YES" if number in seen else "NO")
        seen.add(number)


if __name__ == "__main__":
    main()
