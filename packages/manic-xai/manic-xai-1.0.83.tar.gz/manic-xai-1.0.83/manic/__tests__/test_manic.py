import unittest
from manic import Manic

class TestEndToEnd(unittest.TestCase):

    def test_end_to_end(self):
        # Test end-to-end functionality
        data_instance = [1, 0.5, 'category_a']
        base_counterfactuals = [[1, 0.4, 'category_b'], [1, 0.6, 'category_c']]
        categorical_features = [2]
        immutable_features = []
        feature_ranges = {1: (0, 1), 2: ['category_a', 'category_b', 'category_c']}
        data = [[1, 0.5, 'category_a'], [2, 0.7, 'category_b'], [1, 0.3, 'category_c']]
        predict_fn = lambda x: 1

        # Initialize the Manic instance
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

        # Generate counterfactual
        counterfactual = manic_instance.generate_counterfactuals()

        # Check if the counterfactual is valid
        valid = manic_instance.is_counterfactual_valid(counterfactual)
        self.assertTrue(valid)

if __name__ == '__main__':
    unittest.main()
