import unittest
from Disagreement import Disagreement

class TestDisagreement(unittest.TestCase):
    def test_euclidean_distance(self):
        disagreement = Disagreement(disagreement_method="euclidean_distance",
                                    data_instance=[1, 2, 3],
                                    base_counterfactuals=None,
                                    categorical_features=None,
                                    continuous_feature_ranges=None,
                                    predict_fn=None,
                                    predict_proba_fn=None,
                                    target_class=None,
                                    feature_ranges=[(1, 5), (1, 5), (1, 5)])

        # Test for identical instances
        instance1 = [1, 2, 3]
        instance2 = [1, 2, 3]
        with self.subTest(msg="Test for identical instances"):
            self.assertEqual(disagreement.euclidean_distance(instance1, instance2), 0)

        # Test for completely different instances
        instance1 = [1, 2, 3]
        instance2 = [5, 4, 1]
        with self.subTest(msg="Test for completely different instances"):
            self.assertAlmostEqual(disagreement.euclidean_distance(instance1, instance2), 1.224745, places=3)

        # Test for empty instance (should raise ValueError)
        instance1 = []
        instance2 = [1, 2, 3]
        with self.subTest(msg="Test for empty instance1"):
            with self.assertRaises(AssertionError):
                disagreement.euclidean_distance(instance1, instance2)

        # Test for empty instance (should raise ValueError)
        instance1 = [1, 2, 3]
        instance2 = []
        with self.subTest(msg="Test for empty instance2"):
            with self.assertRaises(AssertionError):
                disagreement.euclidean_distance(instance1, instance2)
                
        # Test for instances with different lengths (should raise ValueError)
        instance1 = [1, 2, 3]
        instance2 = [1, 2]
        with self.subTest(msg="Test for instances with different lengths"):
            with self.assertRaises(AssertionError):
                disagreement.euclidean_distance(instance1, instance2)

        # Test for non-numeric values in instances (should raise ValueError)
        instance1 = [1, 2, 3]
        instance2 = [1, 2, "a"]
        with self.subTest(msg="Test for non-numeric values in instances"):
            with self.assertRaises(AssertionError):
                disagreement.euclidean_distance(instance1, instance2)

    def test_calculate_cosine_distance(self):
        # Test cosine distance for different scenarios
        self.disagreement = Disagreement(disagreement_method="euclidean_distance",
                                    data_instance=[1, 2, 3],
                                    base_counterfactuals=None,
                                    categorical_features=None,
                                    continuous_feature_ranges=None,
                                    predict_fn=None,
                                    predict_proba_fn=None,
                                    target_class=None,
                                    feature_ranges=[(1, 5), (1, 5), (1, 5)])
        
        # Test case 1: Two instances that are the same
        instance1 = [1, 2, 3]
        instance2 = [1, 2, 3]
        with self.subTest(msg="Cosine distance for the same instance should be 0"):
            self.assertEqual(self.disagreement.calculate_cosine_distance(instance1, instance2), 0.0)

        # Test case 2: Two instances that are completely different
        instance1 = [1, 2, 3]
        instance2 = [5, 4, 1]
        with self.subTest(msg="Cosine distance for completely different instances matches manual tested value"):
            self.assertEqual(self.disagreement.calculate_cosine_distance(instance1, instance2), 1.0)

        # Test case 3: Cosine distance for an empty instance
        instance1 = [1, 2, 3]
        instance2 = []
        with self.subTest(msg="Cosine distance with an empty instance should raise an error"):
            with self.assertRaises(AssertionError):
                self.disagreement.calculate_cosine_distance(instance1, instance2)

        # Test case 4: Cosine distance for instances with different lengths
        instance1 = [1, 2, 3]
        instance2 = [4, 5]
        with self.subTest(msg="Cosine distance with instances of different lengths should raise an error"):
            with self.assertRaises(AssertionError):
                self.disagreement.calculate_cosine_distance(instance1, instance2)

        # Test case 5: Cosine distance for instances with non-numeric values
        instance1 = [1, 2, 3]
        instance2 = [4, "hello", 6]
        with self.subTest(msg="Cosine distance with instances containing non-numeric values should raise an error"):
            with self.assertRaises(AssertionError):
                self.disagreement.calculate_cosine_distance(instance1, instance2)

if __name__ == "__main__":
    unittest.main()
