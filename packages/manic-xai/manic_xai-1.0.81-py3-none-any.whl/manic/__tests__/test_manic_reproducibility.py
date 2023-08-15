import unittest
from manic import Manic

class TestManicReproducibility(unittest.TestCase):
    def test_reproducibility(self):
        # Replace the inputs as needed
        data_instance = [...]
        base_counterfactuals = [...]
        categorical_features = [...]
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

        # Create two separate Manic instances with the same seed
        manic_instance1 = Manic(
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

        manic_instance2 = Manic(
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

        # Generate counterfactuals using both instances
        counterfactual1 = manic_instance1.generate_counterfactuals()
        counterfactual2 = manic_instance2.generate_counterfactuals()

        # Assert that the generated counterfactuals are the same when using the same seed
        self.assertEqual(counterfactual1, counterfactual2)

if __name__ == '__main__':
    unittest.main()
