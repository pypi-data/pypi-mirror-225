import unittest
from manic import Manic

class TestManicInitialisation(unittest.TestCase):
    def test_initialise_population_immutable(self):
        # Define a data instance with immutable features
        data_instance = [1, 0.5, 0.2]

        # Replace the other inputs as needed
        base_counterfactuals = [...]
        categorical_features = [...]
        immutable_features = [0, 2]  # Immutable features (for example, features 0 and 2)
        feature_ranges = {...}
        data = [...]
        predict_fn = your_prediction_function

        population_size = 100
        num_generations = 50
        alpha = 0.5
        beta = 0.5
        perturbation_fraction = 0.1
        num_parents = 2
        seed = 42
        verbose = 0
        early_stopping = None
        max_time = None

        # Create the Manic instance
        manic_instance = Manic(
            data_instance,
            base_counterfactuals,
            categorical_features,
            immutable_features,
            feature_ranges,
            data,
            predict_fn,
            population_size=population_size,
            num_generations=num_generations,
            alpha=alpha,
            beta=beta,
            perturbation_fraction=perturbation_fraction,
            num_parents=num_parents,
            seed=seed,
            verbose=verbose,
            early_stopping=early_stopping,
            max_time=max_time
        )

        # initialise the population
        population = manic_instance.initialise_population()

        # Assert that the immutable features in the generated population are the same as the data instance
        for candidate_instance in population:
            for i in immutable_features:
                self.assertEqual(candidate_instance[i], data_instance[i])

    def test_initialise_population_categorical_features(self):
        # Define a data instance with categorical features
        data_instance = [0, 1, 0, 1]

        # Replace the other inputs as needed
        base_counterfactuals = [...]
        categorical_features = [0, 2]  # Categorical features (for example, features 0 and 2)
        immutable_features = [...]
        feature_ranges = {...}
        data = [...]
        predict_fn = your_prediction_function

        population_size = 100
        num_generations = 50
        alpha = 0.5
        beta = 0.5
        perturbation_fraction = 0.1
        num_parents = 2
        seed = 42
        verbose = 0
        early_stopping = None
        max_time = None

        # Create the Manic instance
        manic_instance = Manic(
            data_instance,
            base_counterfactuals,
            categorical_features,
            immutable_features,
            feature_ranges,
            data,
            predict_fn,
            population_size=population_size,
            num_generations=num_generations,
            alpha=alpha,
            beta=beta,
            perturbation_fraction=perturbation_fraction,
            num_parents=num_parents,
            seed=seed,
            verbose=verbose,
            early_stopping=early_stopping,
            max_time=max_time
        )

        # initialise the population
        population = manic_instance.initialise_population()

        # Assert that the categorical features in the generated population are within valid categories
        for candidate_instance in population:
            for i in categorical_features:
                self.assertIn(candidate_instance[i], manic_instance.categories[i])

    def test_initialise_population_continuous_features(self):
        # Define a data instance with continuous features
        data_instance = [0.5, 0.7, 0.3, 0.9]

        # Replace the other inputs as needed
        base_counterfactuals = [...]
        categorical_features = [...]
        immutable_features = [...]
        feature_ranges = {
            0: (0.0, 1.0),
            1: (0.0, 1.0),
            2: (0.0, 1.0),
            3: (0.0, 1.0)
        }  # Continuous feature ranges
        data = [...]
        predict_fn = your_prediction_function

        population_size = 100
        num_generations = 50
        alpha = 0.5
        beta = 0.5
        perturbation_fraction = 0.1
        num_parents = 2
        seed = 42
        verbose = 0
        early_stopping = None
        max_time = None

        # Create the Manic instance
        manic_instance = Manic(
            data_instance,
            base_counterfactuals,
            categorical_features,
            immutable_features,
            feature_ranges,
            data,
            predict_fn,
            population_size=population_size,
            num_generations=num_generations,
            alpha=alpha,
            beta=beta,
            perturbation_fraction=perturbation_fraction,
            num_parents=num_parents,
            seed=seed,
            verbose=verbose,
            early_stopping=early_stopping,
            max_time=max_time
        )

        # initialise the population
        population = manic_instance.initialise_population()

        # Assert that the continuous features in the generated population are within valid ranges
        for candidate_instance in population:
            for i in feature_ranges.keys():
                lower_bound, upper_bound = feature_ranges[i]
                self.assertGreaterEqual(candidate_instance[i], lower_bound)
                self.assertLessEqual(candidate_instance[i], upper_bound)

if __name__ == '__main__':
    unittest.main()
