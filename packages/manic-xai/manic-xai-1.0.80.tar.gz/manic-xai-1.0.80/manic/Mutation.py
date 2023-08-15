import random

class Mutation:
    """
    Mutation class for applying mutation operations to the candidate counterfactuals.

    @param mutation_method: The mutation method to be used ("random_resetting" or "swap_mutation").
    @type mutation_method: str

    @param perturbation_fraction: The rate of mutation
    @type perturbation_fraction: float

    @param feature_ranges: The ranges of each feature in the candidate counterfactuals.
    @type feature_ranges: list of tuple

    Raises:
        ValueError: If the perturbation fraction is not within the range [0, 1].
        ValueError: If the feature_ranges parameter is None or empty.
        Warning: If an invalid mutation method is provided, it defaults to "random_resetting".
    """
    def __init__(self, mutation_method, perturbation_fraction, feature_ranges, categories, categorical_features):
        self.mutation_method = mutation_method
        self.mutate = self.set_mutation(mutation_method)
        self.perturbation_fraction = perturbation_fraction
        self.feature_ranges = feature_ranges
        self.categories = categories
        self.categorical_features = categorical_features

        self.validate_self()

    def __str__(self):
        """
        Return a string representation of the Mutation object.

        @return: String representation of the Mutation object.
        @rtype: str
        """
        mutate_function_name = self.mutate.__name__ if self.mutate else self.mutate
        return f"Mutation Object:\n" \
               f"Mutation Method: {self.mutation_method}\n" \
               f"Perturbation Fraction: {self.perturbation_fraction}\n" \
               f"Feature Ranges: {self.feature_ranges}\n" \
               f"Mutation Function: {mutate_function_name}\n"

    def to_string(self):
        """
        Return a string representation of the Mutation object.

        @return: String representation of the Mutation object.
        @rtype: str
        """
        return str(self)
    
    def set_mutation(self, mutation_method):
        """
        Set the mutation method based on the provided mutation_method.

        @param mutation_method: The mutation method to be used ("random_resetting" or "swap_mutation").
        @type mutation_method: str

        @return: The corresponding mutation method to be used.
        @rtype: callable
        """
        if mutation_method == "random_resetting":
            return self.random_resetting_mutation
        elif mutation_method == "swap_mutation":
            return self.swap_mutation
        else:
            # Default to random_resetting_mutation if the provided method is invalid
            return self.random_resetting_mutation
        
    def random_resetting_mutation(self, offspring):
        """
        Apply random resetting mutation to the offspring.

        @param offspring: The current population of candidate counterfactuals.
        @type offspring: list of list of int

        @return: The mutated offspring.
        @rtype: list of list of int
        """
        new_offspring = []  # Store the mutated offspring
        for i in range(len(offspring)):
            mutated_instance = offspring[i].copy()  # Create a copy of the instance
            for j in range(len(offspring[i])):
                if random.random() < self.perturbation_fraction:
                    if(j in self.categorical_features):
                        category = random.sample(self.categories[j], 1)
                        mutated_instance[j] = category
                    else:
                        lower_bound, upper_bound = self.feature_ranges[j]
                        mutation_value = random.uniform(lower_bound, upper_bound)
                        mutated_instance[j] = max(lower_bound, min(upper_bound, mutation_value))
            new_offspring.append(mutated_instance)
        return new_offspring
    
    # TODO add constraints if keeeping
    def swap_mutation(self, offspring):
        """
        Apply swap mutation to the offspring.

        @param offspring: The current population of candidate counterfactuals.
        @type offspring: list of list of int

        @return: The mutated offspring.
        @rtype: list of list of int
        """
        for i in range(len(offspring)):
            # Randomly select two different feature indices
            feature_indices = random.sample(range(len(offspring[i])), 2)

            # Swap the values of the selected features
            offspring[i][feature_indices[0]], offspring[i][feature_indices[1]] = \
                offspring[i][feature_indices[1]], offspring[i][feature_indices[0]]

        return offspring
    
    def validate_self(self):
        """
        Validate the input parameters.

        Raises:
            ValueError: If the perturbation fraction is not within the range [0, 1].
            ValueError: If the feature_ranges parameter is None or empty.
            Warning: If an invalid mutation method is provided, it defaults to "random_resetting".
        """
        if self.mutation_method not in ["random_resetting", "swap_mutation"]:
            # Default to "random_resetting" if the provided method is invalid
            self.mutation_method = "random_resetting"
            print("Warning: Invalid mutation method given, it must be random_resetting or swap_mutation. Defaulting to random_resetting.")
        
        if self.mutate not in [self.random_resetting_mutation, self.swap_mutation]:
            raise ValueError("Error initializing mutation method, no valid method was set.")
        
        if self.perturbation_fraction is None:
            raise ValueError("Perturbation fraction cannot be None.")
        
        if self.perturbation_fraction < 0 or self.perturbation_fraction > 1:
            raise ValueError("Perturbation fraction must be between 0 and 1.")
        
        if self.feature_ranges is None or len(self.feature_ranges) == 0:
            raise ValueError("Feature ranges must be given.")
