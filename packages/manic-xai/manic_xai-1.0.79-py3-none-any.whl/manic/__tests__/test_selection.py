import numpy as np
import unittest

from Selection import Selection

class TestSelection(unittest.TestCase):
    def setUp(self):
        # Generate random population for 100 instances
        np.random.seed(42)
        self.population = np.random.randint(1, 10, size=(100, 3)).tolist()

        # Generate fitness scores such that the last two instances have the lowest scores
        self.fitness_scores = [0.5] * 98 + [0.1, 0.2]

    def test_select_elites(self):
        # Create a Selection object
        num_parents = 2
        target_class = 0
        population_size = 100
        predict_fn = lambda instance: 0  # Mock predict_fn for testing
        selection = Selection(num_parents, target_class, population_size, predict_fn)

        # Test for elite selection with serial execution
        selection.parallel = False
        with self.subTest(msg="Test select_elites with serial execution"):
            elites = selection.select_elites(self.population, self.fitness_scores)
            self.assertEqual(len(elites), 10)  # Since population size is 100, we expect 10 elites

        # Test for elite selection with parallel execution
        selection.parallel = True
        with self.subTest(msg="Test select_elites with parallel execution"):
            elites = selection.select_elites(self.population, self.fitness_scores)
            self.assertEqual(len(elites), 10)  # Since population size is 100, we expect 10 elites

        # Test for elite selection with a different target_class
        num_parents = 2
        target_class = 1
        population_size = 100
        selection = Selection(num_parents, target_class, population_size, predict_fn)
        selection.parallel = False
        with self.subTest(msg="Test select_elites with different target_class"):
            elites = selection.select_elites(self.population, self.fitness_scores)
            self.assertEqual(len(elites), 0)  # Since there are no instances with target_class 1, we expect 0 elites

        # Test for elite selection with a large population size
        np.random.seed(42)
        large_population = np.random.randint(1, 10, size=(1000, 3)).tolist()
        large_fitness_scores = [0.5] * 998 + [0.1, 0.2]
        num_parents = 2
        target_class = 0
        population_size = 1000
        selection = Selection(num_parents, target_class, population_size, predict_fn)
        selection.parallel = False
        with self.subTest(msg="Test select_elites with large population size"):
            elites = selection.select_elites(large_population, large_fitness_scores)
            self.assertEqual(len(elites), 100)  # Since population size is 1000, we expect 100 elites

        # Test for exceptional cases
        with self.subTest(msg="Test select_elites with empty fitness scores"):
            empty_fitness_scores = []
            with self.assertRaises(ValueError):
                selection.select_elites(self.population, empty_fitness_scores)

        with self.subTest(msg="Test select_elites with empty population"):
            empty_population = []
            with self.assertRaises(ValueError):
                selection.select_elites(empty_population, self.fitness_scores)

        with self.subTest(msg="Test select_elites with different lengths of population and fitness scores"):
            different_lengths_scores = [0.5] * 99
            with self.assertRaises(ValueError):
                selection.select_elites(self.population, different_lengths_scores)

    def test_select_parents(self):
        # Create a Selection object
        num_parents = 2
        target_class = 0
        population_size = 100
        predict_fn = lambda instance: 0  # Mock predict_fn for testing
        selection = Selection(num_parents, target_class, population_size, predict_fn)

        # Set parallel to False to test serial execution
        selection.parallel = False
        
        # Run the selection
        parents = selection.select_parents(self.population, self.fitness_scores)
        
        # Assert that the parents were selected correctly
        self.assertEqual(len(parents), 2)  # Since num_parents is 2, we expect 2 parents
        self.assertEqual(parents, self.population[-2:])  # The last two instances should be selected as parents

    def test_select_parents_parallel(self):
        # Create a Selection object
        num_parents = 2
        target_class = 0
        population_size = 100
        predict_fn = lambda instance: 0  # Mock predict_fn for testing
        selection = Selection(num_parents, target_class, population_size, predict_fn)

        # Set parallel to True to test parallel execution
        selection.parallel = True
        
        # Run the selection
        parents = selection.select_parents(self.population, self.fitness_scores)
        
        # Assert that the parents were selected correctly
        self.assertEqual(len(parents), 2)  # Since num_parents is 2, we expect 2 parents
        self.assertEqual(parents, self.population[-2:])  # The last two instances should be selected as parents

    def test_select_parents_with_different_class(self):
        # Create a Selection object
        num_parents = 2
        target_class = 1
        population_size = 100
        predict_fn = lambda instance: 0  # Mock predict_fn for testing
        selection = Selection(num_parents, target_class, population_size, predict_fn)

        # Set parallel to False to test serial execution
        selection.parallel = False
        
        # Run the selection
        parents = selection.select_parents(self.population, self.fitness_scores) 
        
        # Assert that the parents were selected correctly
        self.assertEqual(len(parents), 2)  # Since num_parents is 2, we expect 2 parents
        self.assertEqual(parents, self.population[-2:])  # The last two instances should be selected as parents

    def test_select_parents_with_large_population_size(self):
        # Generate random population for 1000 instances
        np.random.seed(42)
        large_population = np.random.randint(1, 10, size=(1000, 3)).tolist()
        
        # Generate fitness scores such that the last two instances have the lowest scores
        large_fitness_scores = [0.5] * 998 + [0.1, 0.2]

        # Create a Selection object
        num_parents = 2
        target_class = 0
        population_size = 1000
        predict_fn = lambda instance: 0  # Mock predict_fn for testing
        selection = Selection(num_parents, target_class, population_size, predict_fn)

        # Set parallel to False to test serial execution
        selection.parallel = False
        
        # Run the selection
        parents = selection.select_parents(self.population, self.fitness_scores)
        
        # Assert that the parents were selected correctly
        self.assertEqual(len(parents), 2)  # Since num_parents is 2, we expect 2 parents
        self.assertEqual(parents, self.population[-2:])  # The last two instances should be selected as parents
    
    def test_select_parents_empty_fitness_scores(self):
        # Test exceptional case when fitness scores list is empty
        empty_fitness_scores = []
        num_parents = 2
        target_class = 0
        population_size = 100
        predict_fn = lambda instance: 0  # Mock predict_fn for testing
        selection = Selection(num_parents, target_class, population_size, predict_fn)

        with self.assertRaises(ValueError):
            selection.select_parents(self.population, empty_fitness_scores)

    def test_select_parents_empty_population(self):
        # Test exceptional case when population list is empty
        empty_population = []
        num_parents = 2
        target_class = 0
        population_size = 100
        predict_fn = lambda instance: 0  # Mock predict_fn for testing
        selection = Selection(num_parents, target_class, population_size, predict_fn)

        with self.assertRaises(ValueError):
            selection.select_parents(empty_population, self.fitness_scores)

    def test_select_parents_different_lengths(self):
        # Test exceptional case when population and fitness scores lists have different lengths
        different_lengths_scores = [0.5] * 99
        num_parents = 2
        target_class = 0
        population_size = 100
        predict_fn = lambda instance: 0  # Mock predict_fn for testing
        selection = Selection(num_parents, target_class, population_size, predict_fn)

        with self.assertRaises(ValueError):
            selection.select_parents(self.population, different_lengths_scores)

    def test_negative_num_parents(self):
        # Test exceptional case when num_parents is negative
        num_parents = -1
        target_class = 0
        population_size = 100
        predict_fn = lambda instance: 0  # Mock predict_fn for testing

        with self.assertRaises(ValueError):
            selection = Selection(num_parents, target_class, population_size, predict_fn)

    def test_negative_population_size(self):
        # Test exceptional case when population size is negative
        num_parents = 2  # Reset num_parents to a valid value
        population_size = -1
        target_class = 0
        predict_fn = lambda instance: 0  # Mock predict_fn for testing
        

        with self.assertRaises(ValueError):
            selection = Selection(num_parents, target_class, population_size, predict_fn)

if __name__ == "__main__":
    unittest.main()