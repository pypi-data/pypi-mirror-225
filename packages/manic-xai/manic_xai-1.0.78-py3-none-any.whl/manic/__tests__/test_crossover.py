import unittest
import numpy as np
from Crossover import Crossover

class TestCrossover(unittest.TestCase):
    def setUp(self):
        # Set up the test data
        self.num_parents = 2
        self.population_size = 100
        self.crossover = Crossover(crossover_method="single_point", num_parents=self.num_parents, population_size=self.population_size)
        self.parents = [np.array([1, 2, 3]), np.array([4, 5, 6])]

    def test_single_point_crossover(self):
        with self.subTest("Offspring size equals population_size"):
            offspring = self.crossover.single_point_crossover(self.parents)
            self.assertEqual(len(offspring), self.population_size)

        with self.subTest("Each row in offspring has the same number of features"):
            offspring = self.crossover.single_point_crossover(self.parents)
            num_features = len(offspring[0])
            self.assertTrue(all(len(row) == num_features for row in offspring))

        with self.subTest("num_parents is at least 2"):
            # Set num_parents to 1 and check for ValueError
            self.crossover.num_parents = 1
            with self.assertRaises(ValueError):
                self.crossover.single_point_crossover(self.parents)

        with self.subTest("population size is at least 2"):
            # Set population_size to 1 and check for ValueError
            self.crossover.num_parents = 2
            self.crossover.population_size = 1
            with self.assertRaises(ValueError):
                self.crossover.single_point_crossover(self.parents)

        with self.subTest("len(self.parents) == num_parents"):
            # Set num_parents to 3 and check for ValueError
            self.crossover.num_parents = 3
            with self.assertRaises(ValueError):
                self.crossover.single_point_crossover(self.parents)

if __name__ == "__main__":
    unittest.main()
