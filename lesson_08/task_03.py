"""Минимальное количество лодок: сортировка и два указателя."""


def minimum_boats(weights, capacity):
    if capacity <= 0 or any(w <= 0 or w > capacity for w in weights):
        raise ValueError("Каждый вес должен быть от 1 до грузоподъёмности")
    ordered = sorted(weights)
    left, right = 0, len(ordered) - 1
    boats = 0
    while left <= right:
        if left < right and ordered[left] + ordered[right] <= capacity:
            left += 1
        right -= 1
        boats += 1
    return boats


def main():
    capacity = int(input())
    n = int(input())
    weights = [int(input()) for _ in range(n)]
    print(minimum_boats(weights, capacity))


if __name__ == "__main__":
    main()
