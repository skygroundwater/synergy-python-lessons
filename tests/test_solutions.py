"""Проверки решений и запуск всех 29 программ из командной строки."""

import ast
from collections import deque
from contextlib import redirect_stdout
import copy
from functools import lru_cache
import importlib.util
from io import StringIO
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
MODULES = {}


def load(relative):
    if relative not in MODULES:
        name = relative.replace("/", "_").replace(".py", "")
        spec = importlib.util.spec_from_file_location(name, ROOT / relative)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        MODULES[relative] = module
    return MODULES[relative]


def run_cli(relative, text="", *arguments):
    result = subprocess.run([sys.executable, "-X", "utf8", str(ROOT / relative), *arguments],
                            input=text, text=True, encoding="utf-8", capture_output=True,
                            cwd=ROOT, timeout=10, check=True)
    return result.stdout


class BasicSolutions(unittest.TestCase):
    def test_rectangle_and_digits(self):
        self.assertEqual(load("lesson_04/task_01.py").rectangle(2.5, 3), (7.5, 11.0))
        digits = load("lesson_04/task_02.py")
        self.assertEqual(digits.calculate(46275), -16807.0)
        with self.assertRaises(ZeroDivisionError):
            digits.calculate(11234)
        with self.assertRaises(ValueError):
            digits.calculate(123)

    def test_description_and_vowels(self):
        describe = load("lesson_05/task_01.py").describe
        self.assertEqual(describe(0), "нулевое число")
        self.assertEqual(describe(-3), "отрицательное нечетное число")
        self.assertEqual(describe(190), "положительное четное число")
        self.assertEqual(load("lesson_05/task_02.py").count_letters("banana"),
                         (3, 3, {"a": 3, "e": 0, "i": 0, "o": 0, "u": 0}))

    def test_all_investor_branches(self):
        function = load("lesson_05/task_03.py").investors
        for a, b, expected in [(10, 10, "2"), (10, 9, "Mike"), (9, 10, "Ivan"),
                               (4, 6, "1"), (4, 5, "0")]:
            with self.subTest(a=a, b=b):
                self.assertEqual(function(10, a, b), expected)

    def test_divisor_boundaries(self):
        count_divisors = load("lesson_06/task_02.py").divisor_count
        for number, expected in [(1, 1), (4, 3), (36, 9), (97, 2), (2_000_000_000, 110)]:
            self.assertEqual(count_divisors(number), expected)

    def test_strings(self):
        palindrome = load("lesson_07/task_01.py").is_palindrome
        self.assertTrue(palindrome("шалаш"))
        self.assertTrue(palindrome(""))
        self.assertFalse(palindrome("python"))
        compress = load("lesson_07/task_02.py").compress_spaces
        self.assertEqual(compress("  a   b  "), " a b ")
        self.assertEqual(compress(" " * 1000), " ")

    def test_rotation_changes_original_list(self):
        rotate = load("lesson_08/task_02.py").rotate_right
        numbers = list(range(100_000))
        identity = id(numbers)
        rotate(numbers)
        self.assertEqual(id(numbers), identity)
        self.assertEqual(numbers[:3], [99999, 0, 1])
        self.assertEqual(numbers[-1], 99998)
        one = [7]
        rotate(one)
        self.assertEqual(one, [7])
        rotate([])

    def test_boats_against_exhaustive_pairing(self):
        minimum_boats = load("lesson_08/task_03.py").minimum_boats
        rng = random.Random(4)
        for _ in range(30):
            weights = tuple(rng.randint(1, 10) for _ in range(rng.randint(1, 8)))

            @lru_cache(None)
            def exhaustive(mask):
                if not mask:
                    return 0
                first = (mask & -mask).bit_length() - 1
                rest = mask ^ (1 << first)
                result = 1 + exhaustive(rest)
                for other in range(first + 1, len(weights)):
                    if rest & (1 << other) and weights[first] + weights[other] <= 10:
                        result = min(result, 1 + exhaustive(rest ^ (1 << other)))
                return result

            self.assertEqual(minimum_boats(weights, 10), exhaustive((1 << len(weights)) - 1))

    def test_age_suffixes_and_powers(self):
        suffix = load("lesson_10/task_01.py").get_suffix
        for age, expected in [(0, "лет"), (1, "год"), (2, "года"), (11, "лет"),
                              (14, "лет"), (21, "год"), (24, "года"), (111, "лет")]:
            self.assertEqual(suffix(age), expected)
        values = load("lesson_10/task_02.py").powers_dictionary()
        self.assertEqual(list(values), list(range(10, -6, -1)))
        self.assertEqual(values[0], 1)
        self.assertAlmostEqual(values[-5], -0.00032)

    def test_factorials(self):
        module = load("lesson_11/task_01.py")
        self.assertEqual(module.factorial(0), 1)
        self.assertEqual(module.factorials_from_factorial(3), [720, 120, 24, 6, 2, 1])
        with self.assertRaises(ValueError):
            module.factorial(-1)

    def test_matrices(self):
        module = load("lesson_13/task_01.py")
        self.assertEqual(module.add_matrices([[1, 2], [3, 4]], [[-1, 5], [6, -4]]),
                         [[0, 7], [9, 0]])
        for rows, columns in [(10, 10), (4, 3)]:
            first = module.generate_matrix(rows, columns)
            second = module.generate_matrix(rows, columns)
            result = module.add_matrices(first, second)
            self.assertEqual(len(result), rows)
            self.assertTrue(all(len(row) == columns for row in result))
            for i in range(rows):
                for j in range(columns):
                    self.assertEqual(result[i][j], first[i][j] + second[i][j])
        with self.assertRaises(ValueError):
            module.add_matrices([[1]], [[1, 2]])
        with self.assertRaises(ValueError):
            module.add_matrices([[1], [2, 3]], [[1], [2]])

    def test_recursion_without_loops(self):
        module = load("lesson_14/task_01.py")
        output = StringIO()
        with redirect_stdout(output):
            module.print_list([0, 1, 2])
        self.assertEqual(output.getvalue(), "0\n1\n2\nКонец списка\n")
        tree = ast.parse((ROOT / "lesson_14/task_01.py").read_text(encoding="utf-8"))
        forbidden = (ast.For, ast.While, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
        self.assertFalse(any(isinstance(node, forbidden) for node in ast.walk(tree)))

    def test_inheritance(self):
        first = load("lesson_15/task_01.py")
        bus = first.Autobus("Renaul Logan", 180, 12)
        self.assertIsInstance(bus, first.Transport)
        self.assertEqual(str(bus), "Название автомобиля: Renaul Logan Скорость: 180 Пробег: 12")
        second = load("lesson_15/task_02.py")
        bus = second.Autobus("Renaul Logan", 180, 12)
        self.assertEqual(bus.seating_capacity(), "Вместимость одного автобуса Renaul Logan: 50 пассажиров")
        self.assertIn("42 пассажиров", bus.seating_capacity(42))

    def test_cash_invariants(self):
        from decimal import Decimal
        cash = load("lesson_16/task_01.py").Kassa("0.10")
        cash.top_up("0.20")
        self.assertEqual(cash.amount, Decimal("0.30"))
        cash.top_up(2000)
        self.assertEqual(cash.count_1000(), 2)
        cash.take_away(1000)
        self.assertEqual(cash.count_1000(), 1)
        before = cash.amount
        with self.assertRaises(ValueError):
            cash.take_away(9999)
        self.assertEqual(cash.amount, before)
        with self.assertRaises(ValueError):
            cash.top_up(-1)

    def test_turtle_moves_and_errors(self):
        turtle = load("lesson_16/task_02.py").Turtle(0, 0, 2)
        turtle.go_right()
        turtle.go_up()
        self.assertEqual((turtle.x, turtle.y), (2, 2))
        turtle.go_left()
        turtle.go_down()
        turtle.degrade()
        self.assertEqual((turtle.x, turtle.y, turtle.s), (0, 0, 1))
        with self.assertRaises(ValueError):
            turtle.degrade()
        turtle.evolve()
        self.assertEqual(turtle.s, 2)

    def test_turtle_shortest_paths_against_bfs(self):
        Turtle = load("lesson_16/task_02.py").Turtle

        def exhaustive(target, step):
            queue = deque([((0, 0, step), 0)])
            seen = {(0, 0, step)}
            while queue:
                (x, y, s), cost = queue.popleft()
                if (x, y) == target:
                    return cost
                neighbors = [(x + s, y, s), (x - s, y, s), (x, y + s, s),
                             (x, y - s, s), (x, y, s + 1)]
                if s > 1:
                    neighbors.append((x, y, s - 1))
                for state in neighbors:
                    if state not in seen:
                        seen.add(state)
                        queue.append((state, cost + 1))

        for step in (1, 2, 3):
            turtle = Turtle(0, 0, step)
            for target in ((0, 0), (1, 0), (3, 0), (2, 2), (-2, 1), (4, -1)):
                self.assertEqual(turtle.count_moves(*target), exhaustive(target, step))
                self.assertEqual((turtle.x, turtle.y, turtle.s), (0, 0, step))
        self.assertEqual(Turtle(s=1_000_000).count_moves(1, 0), 3)


class PetDatabase(unittest.TestCase):
    def setUp(self):
        self.module = load("lesson_11/task_02.py")
        self.original = copy.deepcopy(self.module.pets)
        self.original_id = self.module.next_id
        self.module.pets = {}
        self.module.next_id = 1
        self.output = StringIO()
        self.redirect = redirect_stdout(self.output)
        self.redirect.__enter__()

    def tearDown(self):
        self.redirect.__exit__(None, None, None)
        self.module.pets = self.original
        self.module.next_id = self.original_id

    def test_crud_and_monotonic_ids(self):
        with patch("builtins.input", side_effect=["Каа", "питон", "21", "Саша"]):
            first = self.module.create()
        self.assertEqual(first, 1)
        self.assertIn("21 год", self.module.read(first))
        with patch("builtins.input", side_effect=["Каа", "питон", "22", "Иван"]):
            self.assertTrue(self.module.update(first))
        self.assertEqual(self.module.get_pet(first)["Каа"]["Имя владельца"], "Иван")
        self.assertTrue(self.module.delete(first))
        self.assertFalse(self.module.get_pet(first))
        with patch("builtins.input", side_effect=["Кот", "кот", "0", "Олег"]):
            self.assertEqual(self.module.create(), 2)

    def test_missing_records_do_not_crash(self):
        self.assertFalse(self.module.get_pet(99))
        self.assertFalse(self.module.read(99))
        self.assertFalse(self.module.update(99))
        self.assertFalse(self.module.delete(99))
        self.module.pets_list()


class GameTests(unittest.TestCase):
    def setUp(self):
        self.module = load("lesson_23/game.py")
        self.game = self.module.Game(8, 6, seed=3)

    def clear_map(self):
        game = self.game
        game.grid = [[self.module.EMPTY] * game.width for _ in range(game.height)]
        game.grid[0][0] = self.module.HOSPITAL
        game.grid[-1][-1] = self.module.SHOP
        game.fire_ages.clear()

    def test_generation_and_bounds(self):
        game = self.game
        self.assertEqual((len(game.grid), len(game.grid[0])), (6, 8))
        self.assertTrue(game.cells_of_type(self.module.WATER))
        self.assertTrue(game.cells_of_type(self.module.TREE))
        self.assertTrue(game.fire_ages)
        self.assertFalse(game.move(-1, 0))
        self.assertEqual((game.helicopter.x, game.helicopter.y), (0, 0))

    def test_water_and_extinguishing(self):
        self.clear_map()
        game = self.game
        game.helicopter.capacity = 2
        game.grid[0][1] = self.module.WATER
        game.move(1, 0)
        self.assertEqual(game.helicopter.water, 2)
        game.grid[0][2] = self.module.TREE
        self.assertTrue(game.ignite(2, 0))
        self.assertTrue(game.extinguish())
        self.assertEqual((game.helicopter.water, game.helicopter.score), (1, 10))
        self.assertEqual(game.grid[0][2], self.module.TREE)
        self.assertNotIn((2, 0), game.fire_ages)
        self.assertFalse(game.extinguish())
        self.assertEqual(game.helicopter.water, 1)

    def test_burnt_tree_loses_points(self):
        self.clear_map()
        game = self.game
        game.grid[2][3] = self.module.TREE
        game.ignite(3, 2)
        for _ in range(game.FIRE_LIFETIME):
            game.advance()
        self.assertEqual(game.grid[2][3], self.module.EMPTY)
        self.assertEqual(game.helicopter.score, -5)

    def test_hospital_shop_and_lives(self):
        game = self.game
        game.helicopter.health = 20
        game.helicopter.score = 100
        self.assertTrue(game.heal())
        self.assertEqual((game.helicopter.health, game.helicopter.score), (100, 80))
        game.helicopter.x, game.helicopter.y = 7, 5
        self.assertTrue(game.upgrade())
        self.assertEqual((game.helicopter.capacity, game.helicopter.score), (2, 50))
        game.damage(100)
        self.assertEqual((game.helicopter.lives, game.helicopter.health), (2, 100))
        game.damage(100)
        game.damage(100)
        self.assertFalse(game.running)

    def test_storm_damage_and_clouds(self):
        self.clear_map()
        game = self.game
        game.tick = 4
        game.weather = "гроза"
        game.clouds = [(0, 0)]
        game.advance()
        self.assertEqual(game.helicopter.health, 75)
        self.assertTrue(game.covered_by_cloud(1, 1))
        self.assertFalse(game.covered_by_cloud(2, 2))

    def test_save_reload_keeps_future_simulation(self):
        game = self.game
        for _ in range(18):
            game.advance()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "game.json"
            game.save(path)
            restored = self.module.Game.load(path)
            self.assertEqual(json.dumps(game.to_dict(), sort_keys=True),
                             json.dumps(restored.to_dict(), sort_keys=True))
            for _ in range(25):
                game.advance()
                restored.advance()
            self.assertEqual(json.dumps(game.to_dict(), sort_keys=True),
                             json.dumps(restored.to_dict(), sort_keys=True))

    def test_invalid_save_and_dimensions(self):
        with self.assertRaises(ValueError):
            self.module.Game(0, 6)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "game.json"
            data = self.game.to_dict()
            data["grid"] = [["."]]
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.module.Game.load(path)


class CommandLinePrograms(unittest.TestCase):
    def test_every_task_starts_and_returns_expected_output(self):
        cases = [
            ("03/task_01", "желторотый питон\n34\nКаа\n", 'Возраст: 34 года.'),
            ("03/task_02", "A\nB\nC\nD\nHomo sapiens sapiens\n", "A=>B=>C=>D=>Homo sapiens sapiens"),
            ("04/task_01", "2.5\n3\n", "Площадь: 7.5"),
            ("04/task_02", "46275\n", "-16807.0"),
            ("05/task_01", "-3\n", "число не является четным"),
            ("05/task_02", "banana\n", "e: False"),
            ("05/task_03", "10\n4\n6\n", "1\n"),
            ("06/task_01", "5\n0\n1\n0\n-2\n0\n", "3\n"),
            ("06/task_02", "36\n", "9\n"),
            ("06/task_03", "-3\n3\n", "-2 0 2\n"),
            ("07/task_01", "шалаш\n", "yes\n"),
            ("07/task_02", "a   b\n", "a b\n"),
            ("08/task_01", "4\n1\n2\n3\n4\n", "4 3 2 1\n"),
            ("08/task_02", "4\n1 2 3 4\n", "4 1 2 3\n"),
            ("08/task_03", "10\n4\n2\n3\n7\n8\n", "2\n"),
            ("09/task_01", "5\n1 2 2 3 1\n", "3\n"),
            ("09/task_02", "1 2 2 3\n2 3 4\n", "2\n"),
            ("09/task_03", "1 2 1 2 3\n", "NO\nNO\nYES\nYES\nNO\n"),
            ("10/task_01", "Каа\nпитон\n21\nСаша\n", "Возраст питомца: 21 год"),
            ("10/task_02", "", "10: 10000000000"),
            ("11/task_01", "3\n", "[720, 120, 24, 6, 2, 1]"),
            ("11/task_02", "read\n999\nstop\n", "Питомец с таким ID не найден"),
            ("13/task_01", "4\n3\n", "Сумма"),
            ("14/task_01", "", "16\nКонец списка\n"),
            ("15/task_01", "", "Скорость: 180 Пробег: 12"),
            ("15/task_02", "", "50 пассажиров"),
            ("16/task_01", "", "Остаток: 1050"),
            ("16/task_02", "", "Минимум действий до (3, 3):"),
        ]
        for relative, stdin, expected in cases:
            with self.subTest(program=relative):
                self.assertIn(expected, run_cli("lesson_" + relative + ".py", stdin))

    def test_game_headless_demo(self):
        output = run_cli("lesson_23/game.py", "", "--width", "8", "--height", "6",
                         "--seed", "7", "--demo", "100", "--ascii")
        self.assertIn("ЛЕСНОЙ ПАТРУЛЬ", output)
        self.assertIn("Погода:", output)
        self.assertIn("Жизни:", output)

    def test_game_rejects_zero_dimension(self):
        result = subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "lesson_23/game.py"),
                                 "--width", "0", "--height", "6", "--demo", "1"],
                                text=True, encoding="utf-8", capture_output=True, timeout=5)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Ошибка:", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
