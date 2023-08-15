import unittest
from manic import Manic

class TestManicInitialisation(unittest.TestCase):

    def test_default_parameters(self):
        # Create a Manic instance with default parameters
        manic_instance = Manic(
            data_instance=None,
            base_counterfactuals=None,
            categorical_features=None,
            immutable_features=None,
            feature_ranges=None,
            data=None,
            predict_fn=None
        )

        # Assert that the instance is created without errors
        self.assertIsNotNone(manic_instance)

    def test_missing_parameters(self):
        # Test missing required parameters
        with self.assertRaises(ValueError):
            Manic(
                data_instance=None,
                base_counterfactuals=None,
                categorical_features=None,
                immutable_features=None,
                feature_ranges=None,
                data=None,
                predict_fn=None,
                population_size=100,
                num_generations=50,
                alpha=0.5,
                beta=0.5,
                perturbation_fraction=0.1,
                num_parents=2,
                seed=42,
                verbose=0,
                early_stopping=None,
                max_time=None
            )

    def test_faulty_parameters(self):
        # Test faulty parameters
        with self.assertRaises(ValueError):
            # Assuming 'predict_fn' is a function that predicts the target class
            Manic(
                data_instance=None,
                base_counterfactuals=None,
                categorical_features=None,
                immutable_features=None,
                feature_ranges=None,
                data=None,
                predict_fn=None,
                population_size=100,
                num_generations=50,
                alpha=0.5,
                beta=0.5,
                perturbation_fraction=0.1,
                num_parents=2,
                seed=42,
                verbose=0,
                early_stopping=None,
                max_time=None
            )

    def test_successful_initialisation(self):
        # Create a Manic instance with valid parameters
        data_instance = [1, 0.5, 'category_a']
        base_counterfactuals = [[1, 0.4, 'category_b'], [1, 0.6, 'category_c']]
        categorical_features = [2]
        immutable_features = [0]
        feature_ranges = {1: (0, 1), 2: ['category_a', 'category_b', 'category_c']}
        data = [[1, 0.5, 'category_a'], [2, 0.7, 'category_b'], [1, 0.3, 'category_c']]
        predict_fn = lambda x: 0

        manic_instance = Manic(
            data_instance=data_instance,
            base_counterfactuals=base_counterfactuals,
            categorical_features=categorical_features,
            immutable_features=immutable_features,
            feature_ranges=feature_ranges,
            data=data,
            predict_fn=predict_fn,
            population_size=100,
            num_generations=50,
            alpha=0.5,
            beta=0.5,
            perturbation_fraction=0.1,
            num_parents=2,
            seed=42,
            verbose=0,
            early_stopping=None,
            max_time=None
        )

        # Assert that the instance is created without errors
        self.assertIsNotNone(manic_instance)

if __name__ == '__main__':
    unittest.main()
