"""Черепашка с изменяемым шагом и точным поиском минимального числа действий.

count_moves учитывает все действия: четыре перемещения, evolve и degrade.
Позиция самого объекта при расчёте не изменяется. Для поиска используется A*.
"""

from heapq import heappop, heappush
from itertools import count
from math import isqrt


class Turtle:
    def __init__(self, x=0, y=0, s=1):
        if not all(isinstance(value, int) for value in (x, y, s)) or s <= 0:
            raise ValueError("Координаты должны быть целыми, а шаг — положительным целым")
        self.x, self.y, self.s = x, y, s

    def go_up(self):
        self.y += self.s

    def go_down(self):
        self.y -= self.s

    def go_left(self):
        self.x -= self.s

    def go_right(self):
        # В условии здесь опечатка: движение вправо изменяет x, а не y.
        self.x += self.s

    def evolve(self):
        self.s += 1

    def degrade(self):
        if self.s <= 1:
            raise ValueError("Шаг не может стать меньше или равен нулю")
        self.s -= 1

    @staticmethod
    def _lower_bound(distance, step):
        # За k действий нельзя пройти больше k*s + k*(k-1)//2 клеток.
        # Это завышенная оценка достижимого расстояния, поэтому обратная
        # оценка количества действий допустима для A*.
        k = max(0, (isqrt((2 * step - 1) ** 2 + 8 * distance) - (2 * step - 1)) // 2)
        while k * step + k * (k - 1) // 2 < distance:
            k += 1
        return k

    def count_moves(self, x2, y2):
        if not isinstance(x2, int) or not isinstance(y2, int):
            raise ValueError("Целевые координаты должны быть целыми")
        distance = abs(x2 - self.x) + abs(y2 - self.y)
        if distance == 0:
            return 0
        # Два гарантированно достижимых маршрута: уменьшить шаг до 1;
        # либо использовать разность шагов s+1 и s для единичных сдвигов.
        best = min(self.s - 1 + distance, 2 * distance + 1)
        serial = count()
        start = (self.x, self.y, self.s)
        costs = {start: 0}
        queue = [(self._lower_bound(distance, self.s), 0, next(serial), start)]
        while queue:
            estimate, cost, _, state = heappop(queue)
            if estimate >= best:
                break
            if cost != costs[state]:
                continue
            x, y, step = state
            if (x, y) == (x2, y2):
                return cost
            neighbors = [(x + step, y, step), (x - step, y, step),
                         (x, y + step, step), (x, y - step, step),
                         (x, y, step + 1)]
            if step > 1:
                neighbors.append((x, y, step - 1))
            for candidate in neighbors:
                new_cost = cost + 1
                if new_cost >= costs.get(candidate, best):
                    continue
                remaining = abs(x2 - candidate[0]) + abs(y2 - candidate[1])
                lower = self._lower_bound(remaining, candidate[2])
                if new_cost + lower >= best:
                    continue
                costs[candidate] = new_cost
                heappush(queue, (new_cost + lower, new_cost, next(serial), candidate))
        return best


Черепашка = Turtle


if __name__ == "__main__":
    turtle = Turtle(0, 0, 2)
    turtle.go_up()
    turtle.go_right()
    print("Позиция:", turtle.x, turtle.y)
    print("Минимум действий до (3, 3):", turtle.count_moves(3, 3))
