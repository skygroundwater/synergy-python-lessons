"""Генерация и поэлементное сложение прямоугольных матриц."""

import random


def generate_matrix(rows, columns, low=-100, high=100):
    if rows <= 0 or columns <= 0:
        raise ValueError("Размеры матрицы должны быть положительными")
    matrix = []
    for _ in range(rows):
        row = []
        for _ in range(columns):
            row.append(random.randint(low, high))
        matrix.append(row)
    return matrix


def add_matrices(first, second):
    if not first or not second or not first[0] or len(first) != len(second):
        raise ValueError("Нужны две непустые матрицы одинакового размера")
    width = len(first[0])
    if any(len(row) != width for row in first + second):
        raise ValueError("Матрицы должны быть прямоугольными и одинакового размера")
    result = []
    for i in range(len(first)):
        row = []
        for j in range(width):
            row.append(first[i][j] + second[i][j])
        result.append(row)
    return result


def show_matrix(matrix):
    for row in matrix:
        print(*row)


def main():
    rows = int(input("Количество строк (например, 10): "))
    columns = int(input("Количество столбцов (например, 10): "))
    matrix_1 = generate_matrix(rows, columns)
    matrix_2 = generate_matrix(rows, columns)
    matrix_3 = add_matrices(matrix_1, matrix_2)
    for title, matrix in [("Первая матрица", matrix_1),
                          ("Вторая матрица", matrix_2), ("Сумма", matrix_3)]:
        print(title)
        show_matrix(matrix)


if __name__ == "__main__":
    main()
