import unittest
from math import isclose

from tasks.lab2_task1_2 import Lab2_Task1_2

from formulas.probabilities import bernoulli_formula, polynomial_distribution, moivre_laplace_integral_formula

class Lab2Task1_TestCase(unittest.TestCase):
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


class Lab3_TestCase(unittest.TestCase):
    def test_bernoulli(self):
        p = 0.4
        n = 10
        self.assertTrue(isclose(bernoulli_formula(n, p, 6), 0.111476736, abs_tol = 10**-8))
        self.assertTrue(isclose(bernoulli_formula(n, p, 0, 3), 0.382280601, abs_tol = 10**-8))
        self.assertTrue(isclose(bernoulli_formula(n, p, 4, n), 0.617719399, abs_tol = 10**-8))
        # self.assertTrue(isclose(bernoulli_formula(n, p, 5, 7), 0.251793856, abs_tol = 10**-8))

        p = 0.1
        n = 4

        self.assertTrue(isclose(bernoulli_formula(n, p, 3), 0.0036))
        self.assertTrue(isclose(bernoulli_formula(n, p, 0, 2), 0.9963))
        self.assertTrue(isclose(bernoulli_formula(n, p, 3, n), 0.0037))
        self.assertTrue(isclose(bernoulli_formula(n, p, 2, 3), 0.0522))

    def test_polynomial(self):
        self.assertTrue(isclose(
            polynomial_distribution([1, 2, 2, 1], [0.2, 0.3, 0.4, 0.1]), 0.05184))
        self.assertTrue(isclose(
            polynomial_distribution([3, 1, 1], [0.1, 0.3, 0.2]), 0.0012))
        

    def test_integral_formula(self):
        self.assertTrue(isclose(moivre_laplace_integral_formula(70, 100, 0.2, 400), 0.8882, abs_tol=10**-4))
        self.assertTrue(isclose(moivre_laplace_integral_formula(100, 150, 0.75, 150), 0.9909, abs_tol=10**-3))


if __name__ == "__main__":
    unittest.main()