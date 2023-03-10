import unittest
from formulas import (
    CombinationsWithoutRep,
    PlacementWithRep,
    PermutationWithoutRep,
    CombinationsWithRep,
    PermutationWithRep,
)


class CombinationsWithoutRepTestCase(unittest.TestCase):
    def test_values(self):
        args = [
            (10, 18),
            (14, 19),
            (12, 30),
            (15, 30),
            (30, 40),
            (20, 40),
            (33, 67),
            (40, 80),
        ]
        answers = [
            43758,
            11628,
            86493225,
            155117520,
            847660528,
            137846528820,
            14226520737620288370,
            107507208733336176461620,
            52588547141148893628,
        ]
        for i in range(len(args)):
            self.assertEqual(
                CombinationsWithoutRep(*args[i]).result, answers[i]
            )


class PlacementWithRepTestCase(unittest.TestCase):
    def test_values(self):
        args = [
            (7, 12),
            (12, 7),
            (10, 8),
            (15, 11),
            (15, 12),
            (11, 23),
            (9, 33),
        ]
        answers = [
            35831808,
            13841287201,
            1073741824,
            4177248169415651,
            15407021574586368,
            952809757913927,
            46411484401953,
        ]
        for i in range(len(args)):
            self.assertEqual(PlacementWithRep(*args[i]).result, answers[i])


class PermutationTestCase(unittest.TestCase):
    def test_values(self):
        args = [9, 12, 15, 18, 20, 36, 47]
        answers = [
            362880,
            479001600,
            1307674368000,
            6402373705728000,
            2432902008176640000,
            371993326789901217467999448150835200000000,
            258623241511168180642964355153611979969197632389120000000000,
        ]
        for i in range(len(args)):
            self.assertEqual(PermutationWithoutRep(args[i]).result, answers[i])


class CombinationWithRepTestCase(unittest.TestCase):
    def test_values(self):
        args = [
            (5, 10),
            (15, 10),
            (17, 14),
            (32, 19),
            (30, 50),
            (78, 10),
            (60, 15),
        ]
        answers = [
            2002,
            1307504,
            119759850,
            18053528883775,
            5544632834275283414380,
            512916800670,
            456002537343216,
        ]
        for i in range(len(args)):
            self.assertEqual(CombinationsWithRep(*args[i]).result, answers[i])


class PermutationWithRepTestCase(unittest.TestCase):
    def test_values(self):
        args = [
            (2, 3, 5),
            (3, 4, 5),
            (2, 2, 1, 9),
            (10, 8, 2),
            (6, 4, 3, 2, 5),
            (6, 4, 8, 2, 5),
            (6, 8, 9, 12, 5),
        ]
        answers = [
            2520,
            27720,
            60060,
            8314020,
            97772875200,
            92762015346000,
            1347444249443795110608000,
        ]
        for i in range(len(args)):
            self.assertEqual(PermutationWithRep(*args[i]).result, answers[i])


if __name__ == "__main__":
    unittest.main()
