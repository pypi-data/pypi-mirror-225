import unittest
from manic import Manic

class TestIsCounterfactualValid(unittest.TestCase):

    def test_is_counterfactual_valid_valid(self):
        # Test a valid counterfactual
        data_instance = [1, 0.5, 'category_a']
        base_counterfactuals = [[1, 0.4, 'category_b'], [1, 0.6, 'category_c']]
        categorical_features = [2]
        immutable_features = []
        feature_ranges = {1: (0, 1), 2: ['category_a', 'category_b', 'category_c']}
        data = [[1, 0.5, 'category_a'], [2, 0.7, 'category_b'], [1, 0.3, 'category_c']]
        predict_fn = lambda x: 1

        manic_instance = Manic(
            data_instance=data_instance,
            base_counterfactuals=base_counterfactuals,
            categorical_features=categorical_features,
            immutable_features=immutable_features,
            feature_ranges=feature_ranges,
            data=data,
            predict_fn=predict_fn,
            population_size=100
        )

        counterfactual = [2, 0.6, 'category_c']  # Valid counterfactual
        self.assertTrue(manic_instance.is_counterfactual_valid(counterfactual))

    def test_is_counterfactual_valid_invalid_immutable(self):
        # Test an invalid counterfactual with immutable feature changed
        data_instance = [1, 0.5, 'category_a']
        base_counterfactuals = [[1, 0.4, 'category_b'], [1, 0.6, 'category_c']]
        categorical_features = [2]
        immutable_features = [0]
        feature_ranges = {1: (0, 1), 2: ['category_a', 'category_b', 'category_c']}
        data = [[1, 0.5, 'category_a'], [2, 0.7, 'category_b'], [1, 0.3, 'category_c']]
        predict_fn = lambda x: 1

        manic_instance = Manic(
            data_instance=data_instance,
            base_counterfactuals=base_counterfactuals,
            categorical_features=categorical_features,
            immutable_features=immutable_features,
            feature_ranges=feature_ranges,
            data=data,
            predict_fn=predict_fn,
            population_size=100
        )

        counterfactual = [2, 0.6, 'category_c']  # Invalid counterfactual, immutable feature changed
        self.assertFalse(manic_instance.is_counterfactual_valid(counterfactual))

    def test_is_counterfactual_valid_invalid_class(self):
        # Test an invalid counterfactual with unchanged class
        data_instance = [1, 0.5, 'category_a']
        base_counterfactuals = [[1, 0.4, 'category_b'], [1, 0.6, 'category_c']]
        categorical_features = [2]
        immutable_features = []
        feature_ranges = {1: (0, 1), 2: ['category_a', 'category_b', 'category_c']}
        data = [[1, 0.5, 'category_a'], [2, 0.7, 'category_b'], [1, 0.3, 'category_c']]
        predict_fn = lambda x: 0  # Counterfactual should have a different class

        manic_instance = Manic(
            data_instance=data_instance,
            base_counterfactuals=base_counterfactuals,
            categorical_features=categorical_features,
            immutable_features=immutable_features,
            feature_ranges=feature_ranges,
            data=data,
            predict_fn=predict_fn,
            population_size=100
        )

        counterfactual = [2, 0.6, 'category_c']  # Invalid counterfactual, same class
        self.assertFalse(manic_instance.is_counterfactual_valid(counterfactual))

    def test_is_counterfactual_valid_invalid_none(self):
        # Test an invalid counterfactual with None value
        data_instance = [1, 0.5, 'category_a']
        base_counterfactuals = [[1, 0.4, 'category_b'], [1, 0.6, 'category_c']]
        categorical_features = [2]
        immutable_features = []
        feature_ranges = {1: (0, 1), 2: ['category_a', 'category_b', 'category_c']}
        data = [[1, 0.5, 'category_a'], [2, 0.7, 'category_b'], [1, 0.3, 'category_c']]
        predict_fn = lambda x: 1

        manic_instance = Manic(
            data_instance=data_instance,
            base_counterfactuals=base_counterfactuals,
            categorical_features=categorical_features,
            immutable_features=immutable_features,
            feature_ranges=feature_ranges,
            data=data,
            predict_fn=predict_fn,
            population_size=100
        )

        counterfactual = None  # Invalid counterfactual, None value
        self.assertFalse(manic_instance.is_counterfactual_valid(counterfactual))

if __name__ == '__main__':
    unittest.main()
