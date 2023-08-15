import unittest
from manic import Manic

class TestAttribtutes(unittest.TestCase):

    def test_initialize_population_immutable(self):
        # Test for initialization with immutable features
        data_instance = [1, 0.5, 'category_a']
        categorical_features = [2]
        immutable_features = [0]
        feature_ranges = {1: (0, 1), 2: ['category_a', 'category_b', 'category_c']}

        manic_instance = Manic(
            data_instance=data_instance,
            base_counterfactuals=None,
            categorical_features=categorical_features,
            immutable_features=immutable_features,
            feature_ranges=feature_ranges,
            data=None,
            predict_fn=None
        )

        population = manic_instance.initialize_population()

        # Ensure population contains correct number of instances
        self.assertEqual(len(population), manic_instance.population_size)

        # Ensure immutable features are not changed
        for instance in population:
            self.assertEqual(instance[0], data_instance[0])

    def test_initialize_population_categorical(self):
        # Test for initialization with categorical features
        data_instance = [1, 0.5, 'category_a']
        categorical_features = [2]
        immutable_features = []
        feature_ranges = {1: (0, 1), 2: ['category_a', 'category_b', 'category_c']}

        manic_instance = Manic(
            data_instance=data_instance,
            base_counterfactuals=None,
            categorical_features=categorical_features,
            immutable_features=immutable_features,
            feature_ranges=feature_ranges,
            data=None,
            predict_fn=None
        )

        population = manic_instance.initialize_population()

        # Ensure population contains correct number of instances
        self.assertEqual(len(population), manic_instance.population_size)

        # Ensure categorical features are initialized correctly
        for instance in population:
            self.assertIn(instance[2], feature_ranges[2])

    def test_initialize_population_continuous(self):
        # Test for initialization with continuous features
        data_instance = [1, 0.5, 'category_a']
        categorical_features = []
        immutable_features = []
        feature_ranges = {1: (0, 1)}

        manic_instance = Manic(
            data_instance=data_instance,
            base_counterfactuals=None,
            categorical_features=categorical_features,
            immutable_features=immutable_features,
            feature_ranges=feature_ranges,
            data=None,
            predict_fn=None
        )

        population = manic_instance.initialize_population()

        # Ensure population contains correct number of instances
        self.assertEqual(len(population), manic_instance.population_size)

        # Ensure continuous features are initialized within the specified range
        for instance in population:
            self.assertGreaterEqual(instance[1], feature_ranges[1][0])
            self.assertLessEqual(instance[1], feature_ranges[1][1])

    def test_str_representation(self):
        # Create a Manic instance (example values)
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

        # Test the __str__ function
        str_representation = str(manic_instance)

        # Assert that the string representation contains all attributes
        self.assertIn("data_instance: [1, 0.5, 'category_a']", str_representation)
        self.assertIn("base_counterfactuals: [[1, 0.4, 'category_b'], [1, 0.6, 'category_c']]", str_representation)
        self.assertIn("categorical_features: [2]", str_representation)
        self.assertIn("immutable_features: [0]", str_representation)
        self.assertIn("data: [[1, 0.5, 'category_a'], [2, 0.7, 'category_b'], [1, 0.3, 'category_c']]", str_representation)
        self.assertIn("population_size: 100", str_representation)
        self.assertIn("num_generations: 50", str_representation)
        self.assertIn("alpha: 0.5", str_representation)
        self.assertIn("beta: 0.5", str_representation)
        self.assertIn("perturbation_fraction: 0.1", str_representation)
        self.assertIn("num_parents: 2", str_representation)
        self.assertIn("seed: 42", str_representation)
        self.assertIn("verbose: 0", str_representation)
        self.assertIn("early_stopping: None", str_representation)
        self.assertIn("max_time: None", str_representation)

    def test_to_string(self):
            # Create a Manic instance (example values)
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

            # Test the to_string method
            string_representation = manic_instance.to_string()

            # Assert that the string representation contains all attributes
            self.assertIn("data_instance: [1, 0.5, 'category_a']", string_representation)
            self.assertIn("base_counterfactuals: [[1, 0.4, 'category_b'], [1, 0.6, 'category_c']]", string_representation)
            self.assertIn("categorical_features: [2]", string_representation)
            self.assertIn("immutable_features: [0]", string_representation)
            self.assertIn("data: [[1, 0.5, 'category_a'], [2, 0.7, 'category_b'], [1, 0.3, 'category_c']]", string_representation)
            self.assertIn("population_size: 100", string_representation)
            self.assertIn("num_generations: 50", string_representation)
            self.assertIn("alpha: 0.5", string_representation)
            self.assertIn("beta: 0.5", string_representation)
            self.assertIn("perturbation_fraction: 0.1", string_representation)
            self.assertIn("num_parents: 2", string_representation)
            self.assertIn("seed: 42", string_representation)
            self.assertIn("verbose: 0", string_representation)
            self.assertIn("early_stopping: None", string_representation)
            self.assertIn("max_time: None", string_representation)

if __name__ == '__main__':
    unittest.main()
