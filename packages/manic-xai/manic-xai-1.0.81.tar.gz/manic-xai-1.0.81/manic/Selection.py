import numbers
import numpy as np
import concurrent.futures
import random

class Selection:
    """
    Selection class for selecting elites and parents from the population.

    @param num_parents: Number of parents to select in the selection process.
    @type num_parents: int

    @param target_class: The target class that the selection process aims to find.
    @type target_class: int

    @param population_size: Size of the population to be selected from.
    @type population_size: int

    @param predict_fn: The function used for predicting the class label of instances.
    @type predict_fn: callable

    @param parallel: Boolean flag to enable parallel execution of the selection process.
    @type parallel: bool
    """
    def __init__(self, num_parents, target_class, population_size, predict_fn, parallel, tournament_percentage=0.1):
        self.num_parents = num_parents
        self.target_class = target_class
        self.population_size = population_size
        self.predict_fn = predict_fn
        self.parallel = parallel
        self.tournament_percentage = tournament_percentage

        self.validate_self()

    def __str__(self):
        """
        Return a string representation of the Selection object.

        @return: String representation of the Selection object.
        @rtype: str
        """
        predict_fn_name = self.predict_fn.__name__ if self.predict_fn else self.predict_fn
        return f"Selection Object:\n" \
               f"Number of Parents: {self.num_parents}\n" \
               f"Target Class: {self.target_class}\n" \
               f"Population Size: {self.population_size}\n" \
               f"Predict Function: {predict_fn_name}\n" \
               f"Parallel Execution: {self.parallel}\n"

    def to_string(self):
        """
        Return a string representation of the Selection object.

        @return: String representation of the Selection object.
        @rtype: str
        """
        return str(self)
    
    def select_elites(self, population, fitness_scores):
        """
        Select the elite instances from the population based on their fitness scores.

        @param population: The current population of candidate counterfactuals.
        @type population: list of list

        @param fitness_scores: The fitness scores of the candidate counterfactuals.
        @type fitness_scores: list of float

        @return: The elite instances from the population.
        @rtype: list of list
        """
        self.validate_population_and_fitness_scores(population, fitness_scores)
      
        elites = []
        num_elites = int(self.population_size / 10)  # Select top 10% as elites

        # Sort individuals based on fitness score
        sorted_indices = np.argsort(fitness_scores)
        elites_indices = sorted_indices[:num_elites]

        # Use parallel execution only if self.parallel is set to True
        if self.parallel:
            # Use ThreadPoolExecutor for parallel execution
            with concurrent.futures.ThreadPoolExecutor() as executor:
                elite_results = list(executor.map(self.is_elite, elites_indices, [population]*len(elites_indices)))

            # Add elite instances to the elites list
            for idx, is_elite_instance in zip(elites_indices, elite_results):
                if is_elite_instance:
                    elites.append(population[idx])
        else:
            # Run the selection in serial without parallelization
            for idx in elites_indices:
                elite_instance = population[idx]
                elite_class = self.predict_fn(elite_instance)
                if elite_class == self.target_class:
                    elites.append(elite_instance)

        return elites
    
    def is_elite(self, idx, population):
        """
        Check if the instance at the given index is an elite instance.

        @param idx: The index of the instance in the population.
        @type idx: int

        @param population: The current population of candidate counterfactuals.
        @type population: list of list

        @return: True if the instance is an elite, False otherwise.
        @rtype: bool
        """
        elite_instance = population[idx]
        elite_class = self.predict_fn(elite_instance)
        return elite_class == self.target_class

    def select_parents(self, population, fitness_scores):
        """
        Select the parents from the population based on their fitness scores.

        @param population: The current population of candidate counterfactuals.
        @type population: list of list

        @param fitness_scores: The fitness scores of the candidate counterfactuals.
        @type fitness_scores: list of float

        @return: The selected parents from the population.
        @rtype: list of list
        """
        self.validate_population_and_fitness_scores(population, fitness_scores)

        parents = []
        for _ in range(self.num_parents):
            idx = fitness_scores.index(min(fitness_scores))
            parents.append(population[idx])
            fitness_scores[idx] = float('inf')
        return parents

    def tournament_selection(self, population, fitness_scores):
        """
        Select the parents from the population based on tournament selection.

        @param population: The current population of candidate counterfactuals.
        @type population: list of list
        @param fitness_scores: The fitness scores of the candidate counterfactuals.
        @type fitness_scores: list of float
        @param tournament_size: The number of individuals to participate in each tournament.
        @type tournament_size: int
        @return: The selected parents from the population.
        @rtype: list of list
        """

        self.validate_population_and_fitness_scores(population, fitness_scores)

        parents = []
        for _ in range(self.num_parents):

            tournament_size = int(len(population) * self.tournament_percentage)
            # Select `tournament_size` individuals at random
            selected_indices = random.sample(range(len(population)), tournament_size)

            # Get the best among the selected
            best_index = min(selected_indices, key=lambda index: fitness_scores[index])

            parents.append(population[best_index])

            # Optionally: Ensure the same individual isn't selected again
            fitness_scores[best_index] = float('inf')

        return parents
    
    def validate_population_and_fitness_scores(self, population, fitness_scores):
        """
        Validate the population and fitness_scores parameters.

        @param population: The current population of candidate counterfactuals.
        @type population: list of list

        @param fitness_scores: The fitness scores of the candidate counterfactuals.
        @type fitness_scores: list of float

        Raises:
            ValueError: If the population or fitness_scores is empty.
            ValueError: If the size of population does not match the size of fitness scores.
        """
        if len(population) == 0:
            raise ValueError("Population cannot be empty.")
        
        if len(fitness_scores) == 0:
            raise ValueError("Fitness scores cannot be empty.")

        if len(population) != len(fitness_scores):
            raise ValueError("Size of population ({}) does not match size of fitness scores ({}).".format(len(population), len(fitness_scores)))
        
        if len(population) == 0:
            raise ValueError("Population cannot be empty.")
        
    def validate_self(self):
        """
        Validate the input parameters.

        Raises:
            ValueError: If the number of parents is less than 2.
            ValueError: If the population size is less than 1.
            ValueError: If the predict function is not provided.
            ValueError: If the parallel setting is not a Boolean.
            ValueError: If the target class is not a number.
        """
        if self.num_parents < 2:
            raise ValueError("Minimum of 2 parents are required for selection.")
        
        if self.population_size < 1:
            raise ValueError("Population size must be greater than 0.")
        
        if self.predict_fn is None:
            raise ValueError("Predict function must be supplied.")
        
        if not isinstance(self.parallel, bool):
            raise ValueError("Parallel setting must be Boolean True or False.")
        
        if not isinstance(self.target_class, numbers.Number):
            raise ValueError("Target class must be numeric.")
