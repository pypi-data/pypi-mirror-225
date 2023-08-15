import numpy as np

from Manic import Manic

# Example binary classification model
def predict_fn(instance):
    CLASS = rf_classifier.predict([instance])
    return CLASS[0]

# Example data instance to explain (features + prediction)
data_instance = [22,2,3,3,0,1,1,16]

# Example base counterfactuals (you can have multiple base counterfactuals)
base_counterfactuals = np.array([
    [32,2,3,1,0,1,1,16],
    [30,3,3,1,2,1,1,15],
    [39,2,3,3,0,1,1,42]
])

# Example categorical features (indices of categorical features)
categorical_features = [1, 2, 3, 4]

# Example immutable features (indices of immutable features)
immutable_features = [5, 6]

# Example custom feature ranges (dictionary where key is feature index and value is a tuple (lower_bound, upper_bound))
feature_ranges = {
    0: (0, 120),
    7: (0, 168)
}

# Sample data (you should replace this with your actual data)
data = train_data

verbose = 2

num_generations = 300

perturbation_fraction = 0.5

seed = 42

early_stopping = {'patience_generations' : 500, 'found': False}
# Create the Manic instance
manic = Manic(
    data_instance=data_instance,
    base_counterfactuals=base_counterfactuals,
    categorical_features=categorical_features,
    immutable_features=immutable_features,
    feature_ranges=feature_ranges,
    data=data,
    predict_fn=predict_fn,
    verbose=verbose,
    perturbation_fraction=perturbation_fraction,
    num_generations=num_generations,
    seed=seed,
    early_stopping=early_stopping,
    max_time=10
)

# Generate counterfactual explanation
counterfactual = cf_algorithm.generate_counterfactuals()

# Output the counterfactual explanation
print("Original Instance:", data_instance)
print("Counterfactual Explanation:", counterfactual)
print(f"Counterfactual Valid: {cf_algorithm.is_counterfactual_valid(counterfactual)}")
