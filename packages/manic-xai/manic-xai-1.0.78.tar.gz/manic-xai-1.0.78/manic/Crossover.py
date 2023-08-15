import random
import numpy as np

class Crossover:
    """
    Crossover class for performing genetic algorithm crossover operations.
    
    @param crossover_method: The method of crossover to be used.
        Possible values: "single_point", "uniform", or "two_point".
    @type crossover_method: str

    @param num_parents: The number of parents involved in crossover (for multi-parent crossover).
    @type num_parents: int

    @param population_size: The size of the population (number of individuals in the population).
    @type population_size: int

    @param parallel: A boolean flag indicating whether to run crossover in parallel (True/False).
    @type parallel: bool
    """
    def __init__(self, crossover_method, num_parents, population_size, parallel, feature_ranges):
        self.crossover = self.set_crossover_method(crossover_method)
        self.num_parents = num_parents 
        self.population_size = population_size
        self.parallel = parallel
        self.feature_ranges = feature_ranges

        # Validate the input parameters
        self.validate_self()

    def __str__(self):
        """
        Return a string representation of the Crossover object.

        @return: String representation of the Crossover object.
        @rtype: str
        """
        return f"Crossover Object:\n" \
               f"Crossover Method: {self.crossover.__name__}\n" \
               f"Number of Parents: {self.num_parents}\n" \
               f"Population Size: {self.population_size}\n" \
               f"Parallel Execution: {self.parallel}"

    def to_string(self):
        """
        Convert the Crossover object to a string.

        @return: String representation of the Crossover object.
        @rtype: str
        """
        return self.__str__()

    def set_crossover_method(self, crossover_method):
        """
        Set the crossover method based on the provided input.

        @param crossover_method: The method of crossover to be used.
        @type crossover_method: str

        @return: The selected crossover method function.
        @rtype: function
        """
        if crossover_method == "single_point":
            return self.single_point_crossover
        elif crossover_method == "uniform":
            return self.uniform_crossover
        elif crossover_method == "two_point":
            return self.two_point_crossover
        else:
            # Default to uniform crossover if an invalid method is provided
            return self.uniform_crossover

    def single_point_crossover(self, parents):
        """
        Perform single-point crossover to create offspring.

        @param parents: List of parent individuals.
        @type parents: list of numpy arrays

        @return: List of offspring individuals.
        @rtype: list of numpy arrays
        """
        offspring = []
        
        for i in range(self.population_size):
            # Get two parent individuals from the given parents list
            parent1 = parents[i % self.num_parents]
            parent2 = parents[(i + 1) % self.num_parents]
            # Choose a random cut point to combine the genetic material
            cut_point = random.randint(1, len(parent1))
            # Create a child individual by concatenating genetic material from both parents
            child = np.concatenate((parent1[:cut_point], parent2[cut_point:]))
            # Add the child to the offspring list
            offspring.append(child)
        return offspring

    def two_point_crossover(self, parents):
        """
        Perform two-point crossover to create offspring.

        @param parents: List of parent individuals.
        @type parents: list of numpy arrays

        @return: List of offspring individuals.
        @rtype: list of numpy arrays
        """
        offspring = []
        
        for i in range(self.population_size):
            # Get two parent individuals from the given parents list
            parent1 = parents[i % self.num_parents]
            parent2 = parents[(i + 1) % self.num_parents]
            
            # Two random cut points to divide the genetic material for crossover
            cut_point1 = random.randint(0, len(parent1) - 1)
            cut_point2 = random.randint(cut_point1 + 1, len(parent1))
            
            # Create the first child by combining genetic material from both parents
            child1 = np.concatenate((parent1[:cut_point1], parent2[cut_point1:cut_point2], parent1[cut_point2:]))
            
            # Create the second child by combining genetic material from both parents
            child2 = np.concatenate((parent2[:cut_point1], parent1[cut_point1:cut_point2], parent2[cut_point2:]))
            
            # Add both children to the offspring list
            offspring.append(child1)
            offspring.append(child2)
        
        return offspring

    def uniform_crossover(self, parents):
        """
        Perform uniform crossover to create offspring.

        @param parents: List of parent individuals.
        @type parents: list of numpy arrays

        @return: List of offspring individuals.
        @rtype: list of numpy arrays
        """
        offspring = []
        
        for i in range(self.population_size):
            # Get two parent individuals from the given parents list
            parent1 = parents[i % self.num_parents]
            parent2 = parents[(i + 1) % self.num_parents]
            # Create a child individual by randomly selecting genetic material from either parent
            child = []
            
            for j in range(len(parent1)):
                # Randomly select genetic material from either parent1 or parent2 with 50% probability
                if random.random() < 0.5:
                    child.append(parent1[j])
                else:
                    child.append(parent2[j])
                
                lower_bound, upper_bound = self.feature_ranges[j]
                if(child[j] > upper_bound):
                    child[j] = upper_bound
                
                if(child[j] < lower_bound):
                    child[j] = lower_bound

            
            # Add the child to the offspring list
            offspring.append(child)
        
        return offspring

    def validate_self(self):
        """
        Validate the input parameters.

        @raises ValueError: If population size is less than 2 or number of parents is less than 2.
        """
        if self.population_size < 2:
            raise ValueError("Population size must be at least 2.")
        
        if self.num_parents < 2:
            raise ValueError("Number of parents must be at least 2.")