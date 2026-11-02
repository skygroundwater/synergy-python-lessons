"""Лесной патруль: консольная игра о тушении лесных пожаров.

Только стандартная библиотека Python. Запуск: python lesson_23/game.py
Управление: WASD, F — тушение, H — лечение, U — улучшение,
K — сохранить, L — загрузить, Q — выйти. Вода набирается над рекой.
"""

import argparse
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import random
import sys
import time


EMPTY, TREE, FIRE, WATER, HOSPITAL, SHOP = ".", "T", "F", "~", "H", "U"
CELLS = {EMPTY, TREE, FIRE, WATER, HOSPITAL, SHOP}
ICONS = {EMPTY: "🟩", TREE: "🌲", FIRE: "🔥", WATER: "🟦",
         HOSPITAL: "🏥", SHOP: "🏪", "helicopter": "🚁",
         "cloud": "☁️", "storm": "🌩️"}


@dataclass
class Helicopter:
    x: int = 0
    y: int = 0
    capacity: int = 1
    water: int = 0
    health: int = 100
    lives: int = 3
    score: int = 0


class Game:
    FIRE_LIFETIME = 6
    HEAL_COST = 20
    UPGRADE_COST = 30

    def __init__(self, width=12, height=8, seed=None):
        if not 5 <= width <= 50 or not 5 <= height <= 30:
            raise ValueError("Ширина: 5–50, высота: 5–30")
        self.width, self.height = width, height
        self.rng = random.Random(seed)
        self.grid = [[EMPTY for _ in range(width)] for _ in range(height)]
        self.helicopter = Helicopter()
        self.fire_ages = {}
        self.tick = 0
        self.weather = "ясно"
        self.clouds = []
        self.message = "Наберите воду над рекой и потушите пожар клавишей F."
        self.generate_river()
        self.generate_trees(max(1, width * height // 3))
        self.grid[0][0] = HOSPITAL
        self.grid[-1][-1] = SHOP
        self.ignite_random_tree()

    @property
    def running(self):
        return self.helicopter.lives > 0

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def cells_of_type(self, cell):
        return [(x, y) for y in range(self.height) for x in range(self.width)
                if self.grid[y][x] == cell]

    def random_cell(self, cell=EMPTY):
        candidates = self.cells_of_type(cell)
        return self.rng.choice(candidates) if candidates else None

    def generate_river(self):
        x = self.rng.randrange(1, self.width - 1)
        for y in range(self.height):
            new_x = max(1, min(self.width - 2, x + self.rng.choice((-1, 0, 1))))
            for column in range(min(x, new_x), max(x, new_x) + 1):
                self.grid[y][column] = WATER
            x = new_x

    def generate_trees(self, amount=1):
        for _ in range(amount):
            cell = self.random_cell()
            if cell is None:
                break
            x, y = cell
            self.grid[y][x] = TREE

    def ignite(self, x, y):
        if self.in_bounds(x, y) and self.grid[y][x] == TREE:
            self.grid[y][x] = FIRE
            self.fire_ages[(x, y)] = 0
            return True
        return False

    def ignite_random_tree(self):
        cell = self.random_cell(TREE)
        if cell is not None:
            self.ignite(*cell)

    def move(self, dx, dy):
        helicopter = self.helicopter
        x, y = helicopter.x + dx, helicopter.y + dy
        if not self.in_bounds(x, y):
            self.message = "За границы карты вылетать нельзя."
            return False
        helicopter.x, helicopter.y = x, y
        self.message = ""
        if self.grid[y][x] == WATER:
            helicopter.water = helicopter.capacity
            self.message = "Резервуары наполнены водой."
        elif self.grid[y][x] == HOSPITAL:
            self.message = f"Госпиталь: H — восстановить здоровье за {self.HEAL_COST} очков."
        elif self.grid[y][x] == SHOP:
            self.message = f"Магазин: U — добавить резервуар за {self.UPGRADE_COST} очков."
        return True

    def extinguish(self):
        helicopter = self.helicopter
        if helicopter.water == 0:
            self.message = "Нет воды. Пролетите над рекой."
            return False
        positions = [(helicopter.x, helicopter.y),
                     (helicopter.x + 1, helicopter.y), (helicopter.x - 1, helicopter.y),
                     (helicopter.x, helicopter.y + 1), (helicopter.x, helicopter.y - 1)]
        for x, y in positions:
            if self.in_bounds(x, y) and self.grid[y][x] == FIRE:
                self.grid[y][x] = TREE
                self.fire_ages.pop((x, y), None)
                helicopter.water -= 1
                helicopter.score += 10
                self.message = "Дерево спасено! +10 очков."
                return True
        self.message = "Поблизости нет пожара: подлетите к горящему дереву."
        return False

    def heal(self):
        helicopter = self.helicopter
        if self.grid[helicopter.y][helicopter.x] != HOSPITAL:
            self.message = "Для лечения прилетите в госпиталь H / 🏥."
            return False
        if helicopter.health == 100:
            self.message = "Здоровье уже полное."
            return False
        if helicopter.score < self.HEAL_COST:
            self.message = "Недостаточно очков для лечения."
            return False
        helicopter.score -= self.HEAL_COST
        helicopter.health = 100
        self.message = "Здоровье восстановлено."
        return True

    def upgrade(self):
        helicopter = self.helicopter
        if self.grid[helicopter.y][helicopter.x] != SHOP:
            self.message = "Для улучшения прилетите в магазин U / 🏪."
            return False
        if helicopter.score < self.UPGRADE_COST:
            self.message = "Недостаточно очков для улучшения."
            return False
        helicopter.score -= self.UPGRADE_COST
        helicopter.capacity += 1
        self.message = "Добавлен резервуар. Заполните его над рекой."
        return True

    def damage(self, amount):
        helicopter = self.helicopter
        helicopter.health = max(0, helicopter.health - amount)
        if helicopter.health == 0:
            helicopter.lives -= 1
            if self.running:
                helicopter.x, helicopter.y = 0, 0
                helicopter.health = 100
                helicopter.water = 0
                self.message = "Вертолёт потерян. Новый вылет из госпиталя."
            else:
                self.message = "Жизни закончились. Игра окончена."

    def covered_by_cloud(self, x, y):
        return any(cx <= x < cx + 2 and cy <= y < cy + 2 for cx, cy in self.clouds)

    def advance(self):
        if not self.running:
            return
        self.tick += 1
        for (x, y), age in list(self.fire_ages.items()):
            age += 1
            if age >= self.FIRE_LIFETIME:
                self.grid[y][x] = EMPTY
                del self.fire_ages[(x, y)]
                self.helicopter.score -= 5
                continue
            self.fire_ages[(x, y)] = age
            if age >= 2:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if self.rng.random() < 0.18:
                        self.ignite(x + dx, y + dy)
        if self.tick % 4 == 0:
            self.generate_trees(2)
        if self.tick % 7 == 0:
            self.ignite_random_tree()
        if self.tick % 15 == 0:
            self.weather = self.rng.choice(("ясно", "облачно", "гроза"))
            self.clouds = [] if self.weather == "ясно" else [
                (self.rng.randrange(self.width), self.rng.randrange(self.height))
                for _ in range(max(1, self.width // 4))]
        if self.tick % 3 == 0:
            self.clouds = [((x + 1) % self.width, y) for x, y in self.clouds]
        if self.weather == "гроза" and self.tick % 5 == 0:
            for x, y in self.clouds:
                self.ignite(x, y)
            if self.covered_by_cloud(self.helicopter.x, self.helicopter.y):
                self.damage(25)
        helicopter = self.helicopter
        if self.grid[helicopter.y][helicopter.x] == FIRE:
            self.damage(10)

    def action(self, key):
        key = key.lower()
        directions = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
        if key in directions:
            return self.move(*directions[key])
        if key in ("f", " "):
            return self.extinguish()
        if key == "h":
            return self.heal()
        if key == "u":
            return self.upgrade()
        return False

    def render(self, ascii_mode=False):
        helicopter = self.helicopter
        lines = ["ЛЕСНОЙ ПАТРУЛЬ", f"Тик: {self.tick} | Погода: {self.weather} | "
                 f"Очки: {helicopter.score} | Здоровье: {helicopter.health}/100 | "
                 f"Жизни: {helicopter.lives} | Вода: {helicopter.water}/{helicopter.capacity}"]
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = self.grid[y][x]
                if (x, y) == (helicopter.x, helicopter.y):
                    symbol = "@" if ascii_mode else ICONS["helicopter"]
                elif self.covered_by_cloud(x, y):
                    symbol = ("!" if self.weather == "гроза" else "o") if ascii_mode else ICONS[
                        "storm" if self.weather == "гроза" else "cloud"]
                else:
                    symbol = cell if ascii_mode else ICONS[cell]
                row.append(symbol)
            lines.append(" ".join(row))
        lines += ["WASD: полёт | F/пробел: тушить | H: лечение | U: улучшение",
                  "K: сохранить | L: загрузить | Q: выход", self.message]
        if ascii_mode:
            lines.append("@: вертолёт, T: дерево, F: пожар, ~: вода, H: госпиталь, U: магазин")
        return "\n".join(lines)

    def to_dict(self):
        return {"version": 1, "width": self.width, "height": self.height,
                "grid": self.grid, "helicopter": asdict(self.helicopter),
                "fires": [[x, y, age] for (x, y), age in self.fire_ages.items()],
                "tick": self.tick, "weather": self.weather, "clouds": self.clouds,
                "rng_state": self.rng.getstate()}

    def save(self, filename="savegame.json"):
        path = Path(filename)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(self.to_dict(), ensure_ascii=False), encoding="utf-8")
        temporary.replace(path)
        self.message = f"Игра сохранена: {path}"

    @classmethod
    def load(cls, filename="savegame.json"):
        data = json.loads(Path(filename).read_text(encoding="utf-8"))
        if data.get("version") != 1:
            raise ValueError("Неизвестный формат сохранения")
        game = cls(data["width"], data["height"], seed=0)
        grid = data["grid"]
        if (len(grid) != game.height or any(len(row) != game.width for row in grid)
                or any(cell not in CELLS for row in grid for cell in row)):
            raise ValueError("Повреждена карта в сохранении")
        helicopter = Helicopter(**data["helicopter"])
        if (not game.in_bounds(helicopter.x, helicopter.y) or helicopter.capacity < 1
                or not 0 <= helicopter.water <= helicopter.capacity
                or not 0 <= helicopter.health <= 100 or not 0 <= helicopter.lives <= 3):
            raise ValueError("Повреждены параметры вертолёта")
        game.grid, game.helicopter = grid, helicopter
        game.fire_ages = {}
        for x, y, age in data["fires"]:
            if (not game.in_bounds(x, y) or grid[y][x] != FIRE
                    or not 0 <= age < cls.FIRE_LIFETIME):
                raise ValueError("Повреждена информация о пожарах")
            game.fire_ages[(x, y)] = age
        if set(game.cells_of_type(FIRE)) != set(game.fire_ages):
            raise ValueError("Не совпадает список пожаров и карта")
        if data["weather"] not in ("ясно", "облачно", "гроза") or data["tick"] < 0:
            raise ValueError("Повреждены параметры погоды или времени")
        game.tick, game.weather = data["tick"], data["weather"]
        game.clouds = [tuple(cell) for cell in data["clouds"]]
        if any(not game.in_bounds(*cell) for cell in game.clouds):
            raise ValueError("Облака находятся за границей карты")

        def nested_tuple(value):
            return tuple(nested_tuple(item) for item in value) if isinstance(value, list) else value

        game.rng.setstate(nested_tuple(data["rng_state"]))
        game.message = "Сохранение загружено."
        return game


class Keyboard:
    """Неблокирующий ввод с восстановлением настроек терминала после выхода."""

    def __enter__(self):
        self.original = None
        if os.name != "nt":
            import termios
            import tty
            self.original = termios.tcgetattr(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())
        return self

    def read(self):
        if os.name == "nt":
            import msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getwch()
                if key in ("\x00", "\xe0"):
                    msvcrt.getwch()
                    return None
                return key
            return None
        import select
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
        return None

    def __exit__(self, *error):
        if self.original is not None:
            import termios
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.original)


def main():
    parser = argparse.ArgumentParser(description="Лесной патруль — тушение пожаров вертолётом")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--ascii", action="store_true", help="Символы вместо эмодзи")
    parser.add_argument("--demo", type=int, default=0, help="N автоматических тиков без ожидания")
    parser.add_argument("--load", action="store_true", help="Сразу загрузить сохранение")
    parser.add_argument("--save-file", default="savegame.json")
    args = parser.parse_args()
    interactive = sys.stdin.isatty() and not args.demo
    width = 12 if args.width is None else args.width
    height = 8 if args.height is None else args.height
    if interactive and not args.load:
        if args.width is None:
            width = int(input("Ширина поля 5–50 [12]: ") or "12")
        if args.height is None:
            height = int(input("Высота поля 5–30 [8]: ") or "8")
    try:
        game = Game.load(args.save_file) if args.load else Game(width, height, args.seed)
        if args.demo:
            for _ in range(max(0, args.demo)):
                game.action(game.rng.choice("wasdff"))
                game.advance()
                if not game.running:
                    break
            print(game.render(args.ascii))
            return

        def act(key):
            nonlocal game
            if key.lower() == "k":
                game.save(args.save_file)
            elif key.lower() == "l":
                try:
                    game = Game.load(args.save_file)
                except (OSError, ValueError, KeyError, TypeError) as error:
                    game.message = f"Не удалось загрузить игру: {error}"
            else:
                game.action(key)

        if not interactive:
            print(game.render(args.ascii))
            for line in sys.stdin:
                key = line.strip().lower()
                if key == "q":
                    break
                act(key)
                game.advance()
                print(game.render(args.ascii))
                if not game.running:
                    break
            return

        with Keyboard() as keyboard:
            next_tick = time.monotonic() + 1
            redraw = True
            while game.running:
                key = keyboard.read()
                if key is not None:
                    if key.lower() == "q" or key == "\x1b":
                        break
                    act(key)
                    redraw = True
                if time.monotonic() >= next_tick:
                    game.advance()
                    next_tick = time.monotonic() + 1
                    redraw = True
                if redraw:
                    print("\033[2J\033[H" + game.render(args.ascii), end="\n", flush=True)
                    redraw = False
                time.sleep(0.03)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Ошибка:", error, file=sys.stderr)
        raise SystemExit(1)
    except KeyboardInterrupt:
        print("\nИгра завершена.")


if __name__ == "__main__":
    main()
