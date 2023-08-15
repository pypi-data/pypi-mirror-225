import random
import heapq
import numpy as np

from Baseline import Baseline
from Disagreement import Disagreement
from Evaluation import Evaluation
from Selection import Selection
from Utility import Utility

class Initialise:
    def __init__(self, disagreement_method, data_instance, base_counterfactuals, predict_fn, predict_proba_fn, seed, population_size, categorical_features, feature_ranges, immutable_features, data, class_labels, theta, alpha, beta, num_parents, verbose, labels, parallel):
        self.seed = seed
        self.population_size = population_size
        self.base_counterfactuals = base_counterfactuals
        self.data = data
        self.class_labels = class_labels
        self.categorical_features = categorical_features
        self.data_instance = data_instance
        self.parallel = parallel
        self.immutable_features_set = set(immutable_features)
        self.categories = self.get_categories(categorical_features)
        self.feature_ranges = self.get_feature_ranges(feature_ranges)
        self.target_class = 1 - predict_fn(data_instance) #TODO don't assume binary classification
        self.disagreement = Disagreement(disagreement_method, data_instance, base_counterfactuals, categorical_features, feature_ranges, predict_fn, predict_proba_fn, self.target_class, self.feature_ranges)
        self.instance_probability = predict_proba_fn(data_instance)
        self.evaluation = Evaluation(alpha, beta, predict_proba_fn, self.instance_probability, base_counterfactuals, self.disagreement, data_instance, theta, parallel)
        self.selection = Selection(num_parents, self.target_class, population_size, predict_fn, parallel)
        self.utils = Utility(data_instance, self.categories, immutable_features, self.target_class, verbose, predict_fn, self.disagreement, base_counterfactuals, self.evaluation, labels)
        self.population = self.initialise_population()
        self.baseline = Baseline(self.disagreement, base_counterfactuals, data_instance)

    def weighted_random_choice(self, options, weights):
        return random.choices(options, weights, k=1)[0]

    def initialise_population(self):
        random.seed(self.seed)
        population = []
        options = [self.generate_random_instance, self.nearest_unlike_neighbors, self.randomly_sample_counterfactual]
        weights = [0.5, 0.2, 0.3]  # These should add up to 1

        for _ in range(int(self.population_size / 2)):
            choice = self.weighted_random_choice(options, weights)
            candidate = choice()
            population.append(candidate)

        return population
    
    def randomly_sample_counterfactual(self):
        return random.choice(self.base_counterfactuals)
    
    def get_feature_ranges(self, continuous_feature_ranges):
        feature_ranges = []
        for i in range(len(self.data_instance)):
            if i in self.immutable_features_set:
                # For immutable features, the range is a single value (the current value)
                feature_ranges.append((self.data_instance[i], self.data_instance[i]))
            elif i in self.categorical_features:
                LOWER_BOUND = min(self.categories[i])
                UPPER_BOUND = max(self.categories[i])
                feature_ranges.append((LOWER_BOUND, UPPER_BOUND))
            elif i in list(continuous_feature_ranges.keys()):
                feature_ranges.append(continuous_feature_ranges[i])
            else:
                LOWER_BOUND = min(self.data[:, i]) - (min(self.data[:, i]) / 10)
                UPPER_BOUND = max(self.data[:, i]) + (max(self.data[:, i]) / 10)
                feature_ranges.append((LOWER_BOUND, UPPER_BOUND))

        return feature_ranges
    
    def generate_random_instance(self):
        candidate_instance = []

        for i, (min_val, max_val) in enumerate(self.feature_ranges):
            if i in self.immutable_features_set:
                # For immutable features, use the original value
                candidate_instance.append(min_val)
            elif i in self.categorical_features:
                possible_values = sorted(set(int(data[i]) for data in self.data))
                candidate_instance.append(random.choice(possible_values))
            else:
                candidate_value = random.uniform(min_val, max_val)
                candidate_instance.append(max(min_val, min(max_val, candidate_value)))

        return candidate_instance
    
    def get_categories(self, categorical_features):
        categories = {}
        for feature in categorical_features:
            options = np.unique(self.data[:,feature])
            categories[feature] = options

        return categories
    
    def nearest_unlike_neighbors(self):
        unlike_neighbors = []
        distances = []

        for i, instance in enumerate(self.data):
            if self.target_class != self.class_labels[i]:
                distance = self.disagreement.euclidean_distance(self.data_instance, instance)
                distances.append((distance, i))  # Store both distance and index

        # Use heapq to efficiently find the n smallest distances and their corresponding indices
        smallest_distances = heapq.nsmallest(int(self.population_size / 2), distances)

        # Get the actual instances for the smallest distances
        for distance, index in smallest_distances:
            neighbor = self.data[index]
            unlike_neighbors.append(neighbor)

        return random.choice(unlike_neighbors)