"""Количество нулей среди N введённых целых чисел."""


def main():
    n = int(input())
    zeros = 0
    for _ in range(n):
        if int(input()) == 0:
            zeros += 1
    print(zeros)


if __name__ == "__main__":
    main()
