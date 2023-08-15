import unittest
import random
from Mutation import Mutation

class TestMutation(unittest.TestCase):
    def setUp(self):
        # Sample feature_ranges for testing
        self.feature_ranges = [(0, 1), (-1, 1), (5, 10)]

    def generate_random_offspring(self, length=100):
        # Generate random offspring for testing
        offspring = []
        for _ in range(length):
            instance = [random.uniform(lower, upper) for lower, upper in self.feature_ranges]
            offspring.append(instance)
        return offspring

    def test_random_resetting_mutation(self):
        # Initialize Mutation with "random_resetting" method
        mutation_method = "random_resetting"
        perturbation_fraction = 0.5
        mutation = Mutation(mutation_method, perturbation_fraction, self.feature_ranges)

        # Test case 1: Random mutation for all features
        offspring = self.generate_random_offspring()
        with self.subTest(msg="Test mutation occurred"):
            mutated_offspring = mutation.random_resetting_mutation(offspring)
            self.assertNotEqual(mutated_offspring, offspring)

        # Test case 2: No mutation if perturbation_fraction is 0
        perturbation_fraction = 0.0
        mutation = Mutation(mutation_method, perturbation_fraction, self.feature_ranges)
        with self.subTest(msg="Test case no mutation"):
            mutated_offspring = mutation.random_resetting_mutation(offspring)
            self.assertEqual(mutated_offspring, offspring)

        # Test case 3: All features should be within the given ranges
        perturbation_fraction = 1.0
        mutation = Mutation(mutation_method, perturbation_fraction, self.feature_ranges)
        with self.subTest(msg="Test valid ranges"):
            mutated_offspring = mutation.random_resetting_mutation(offspring)
            for i in range(len(mutated_offspring)):
                for j in range(len(mutated_offspring[i])):
                    lower_bound, upper_bound = self.feature_ranges[j]
                    self.assertTrue(lower_bound <= mutated_offspring[i][j] <= upper_bound)

        # Test case 4: Offspring with invalid features should be clipped to the valid range
        perturbation_fraction = 1.0
        mutation = Mutation(mutation_method, perturbation_fraction, self.feature_ranges)
        bad_offspring = offspring
        bad_offspring[0] = [66, 300, -100]
        bad_offspring[1] = [100, -400, -1400]
        bad_offspring[2] = [1300, 0, 5]
        with self.subTest(msg="Test clipping"):
            mutated_offspring = mutation.random_resetting_mutation(bad_offspring)
            for i in range(len(mutated_offspring)):
                for j in range(len(mutated_offspring[i])):
                    lower_bound, upper_bound = self.feature_ranges[j]
                    self.assertTrue(lower_bound <= mutated_offspring[i][j] <= upper_bound)

    def test_validate_self(self):
        # Test case for invalid mutation_method
        mutation_method = "invalid_method"
        perturbation_fraction = 0.5
        feature_ranges = [(0, 1), (-1, 1), (5, 10)]

        with self.subTest("Invalid mutation_method"):
            with self.assertRaises(Warning) as cm:
                Mutation(mutation_method, perturbation_fraction, feature_ranges)
            self.assertEqual(str(cm.exception), "Invalid mutation method given, it must be random_resetting or swap_mutation. Defaulting to random_resetting.")

        # Test case for invalid perturbation_fraction
        mutation_method = "random_resetting"
        perturbation_fraction = 1.5  # Invalid value

        with self.subTest("Invalid perturbation_fraction"):
            with self.assertRaises(ValueError) as cm:
                Mutation(mutation_method, perturbation_fraction, feature_ranges)
            self.assertEqual(str(cm.exception), "Perturbation fraction must be between 0 and 1.")

        # Test case for invalid feature_ranges
        mutation_method = "random_resetting"
        perturbation_fraction = 0.5
        feature_ranges = []  # Invalid value

        with self.subTest("Invalid feature_ranges"):
            with self.assertRaises(ValueError) as cm:
                Mutation(mutation_method, perturbation_fraction, feature_ranges)
            self.assertEqual(str(cm.exception), "Feature ranges must be given.")

if __name__ == "__main__":
    unittest.main()
