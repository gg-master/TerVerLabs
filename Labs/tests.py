import unittest
from math import isclose

from tasks.lab2_task1_2 import Lab2_Task1_2


class Task1_TestCase(unittest.TestCase):
    def test_values(self):
        args = [
            [0.6, 0, 0.7, 0, 0.8],
            [0.8, 0.6, 0, 0.7, 0.9],
            [0.5, 0.4, 0.6, 0.8, 0.7],
            [0.6, 0.8, 0.7, 0.9, 0.6]
        ]
        results = [0.336, 0.6336, 0.3332, 0.35784]
        for i in range(len(args)):
            self.assertTrue(isclose(Lab2_Task1_2.task1_formula(*args[i]), results[i]))


if __name__ == "__main__":
    unittest.main()