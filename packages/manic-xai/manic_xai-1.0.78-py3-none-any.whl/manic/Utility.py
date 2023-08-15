import decimal
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class Utility:
    """
    Utility class for formatting counterfactuals, checking their validity, printing results, and computing the disagreement matrix.

    @param data_instance: The instance to be explained.
    @type data_instance: list

    @param categories: A dictionary containing the possible categories for each categorical feature.
    @type categories: dict

    @param immutable_features: A set of indices of features that are immutable and cannot be changed in counterfactuals.
    @type immutable_features: set

    @param target_class: The target class that the counterfactuals aim to achieve.
    @type target_class: int

    @param verbose: An integer representing the verbosity level for printing messages during the counterfactual generation process.
    @type verbose: int

    @param predict_fn: The function used for predicting the class label of instances.
    @type predict_fn: callable

    @param disagreement: The disagreement object used for calculating disagreement scores.
    @type disagreement: Disagreement

    @param base_counterfactuals: The base counterfactuals used in the counterfactual generation process.
    @type base_counterfactuals: list of list

    @param labels: Labels for the base counterfactuals, used for result printing.
    @type labels: list
    """
    def __init__(self, data_instance, categories, immutable_features, target_class, verbose, predict_fn, disagreement, base_counterfactuals, labels):
        self.data_instance = data_instance
        self.categories = categories
        self.immutable_features = immutable_features
        self.target_class = target_class
        self.verbose = verbose
        self.predict_fn = predict_fn
        self.disagreement = disagreement
        self.base_counterfactuals = base_counterfactuals
        self.labels = labels

    def format_counterfactual(self, counterfactual):
        """
        Format the counterfactual by rounding numerical values and converting decimal values to integers.

        @param counterfactual: The counterfactual to be formatted.
        @type counterfactual: list

        @return: The formatted counterfactual.
        @rtype: list
        """
        formatted_counterfactual = []
        for i in range(len(counterfactual)):
            if i in self.categories:
                formatted_counterfactual.append(round(counterfactual[i]))
            else:
                decimal_feature = decimal.Decimal(str(self.data_instance[i]))
                decimal_places = decimal_feature.as_tuple().exponent * -1

                if decimal_places == 0:
                    formatted_counterfactual.append(int(counterfactual[i]))
                else:
                    formatted_counterfactual.append(round(counterfactual[i], decimal_places))

        return formatted_counterfactual
    
    def is_counterfactual_valid(self, counterfactual):
        """
        Check the validity of a counterfactual.

        @param counterfactual: The counterfactual to be validated.
        @type counterfactual: list

        @return: True if the counterfactual is valid, False otherwise.
        @rtype: bool
        """
        # Check if the counterfactual is not None
        if counterfactual is None:
            if self.verbose > 0:
                print("Invalid Counterfactual: None value generated as counterfactual.")
            return False

        # Check if any immutable features are changed
        for i in self.immutable_features:
            if counterfactual[i] != self.data_instance[i]:
                if self.verbose > 0:
                    print(f"Invalid Counterfactual: Feature at index {i} is immutable and cannot be changed.")
                return False

        # Check if the class is equal to the target class
        prediction = self.predict_fn(counterfactual)
        if prediction != self.target_class:
            if self.verbose > 0:
                print(f"Invalid Counterfactual: Predicted class ({prediction}) is not the target class ({self.target_class}).")
            return False

        # All conditions are met, counterfactual is valid
        if self.verbose > 0:
            print("Valid Counterfactual: No immutable features were changed and the counterfactual causes the correct prediction change.")

        return True
    
    def print_results(self, best_counterfactual, best_fitness, num_generations, generation_found, time_taken, time_found, cpu_cycles, proximity_score, sparsity_score, number_of_changes, disagreement_score):
        """
        Print the results of the counterfactual generation process.

        @param best_counterfactual: The best counterfactual found during the generation process.
        @type best_counterfactual: list

        @param best_fitness: The fitness score of the best counterfactual.
        @type best_fitness: float

        @param num_generations: The total number of generations that were evaluated during the process.
        @type num_generations: int

        @param generation_found: The generation at which the best counterfactual was found.
        @type generation_found: int

        @param time_taken: The total time taken to search for the counterfactual.
        @type time_taken: float

        @param time_found: The time taken to find the best counterfactual.
        @type time_found: float

        @param cpu_cycles: The total CPU cycles ran during the search process.
        @type cpu_cycles: float

        @param proximity_score: The proximity score between the meta-counterfactual and the instance explained.
        @type cpu_cycles: float

        @param sparsity_score: The sparsity score of the meta-counterfactual.
        @type cpu_cycles: float

        @param number_of_changes: The number of feature differences between the meta-counterfactual and the instance explained.
        @type cpu_cycles: int

        @param disagreement_score: The average disagreement score between the meta-counterfactual and the base counterfactuals.
        @type cpu_cycles: float
        """
        print("\n------ Counterfactual Generation Results ------")
        if best_counterfactual is not None:
            print(f"{np.array2string(np.array(best_counterfactual), separator=', ')}: Best Counterfactual 👑")
            print(f"{np.array2string(np.array(self.data_instance), separator=', ')}: Instance Explained 🔍")
            for i, counterfactual in enumerate(self.base_counterfactuals):
                print(f"{np.array2string(counterfactual, separator=', ')}: {self.labels[i]}")
            print("Proximity from Data Instance:", proximity_score)
            print("Sparsity:", sparsity_score)
            print("Number of changes made to produce the counterfactual:", number_of_changes)
            print("Disagreement Score against Base Counterfactuals:", disagreement_score)
            print("Number of Generations:", num_generations)
            print(f"Counterfactual found after {generation_found + 1} generations")
            print("Fitness Score:", best_fitness)
            print(f"Time taken to find counterfactual: {time_found:.4f} seconds")
            print(f"Total time searched: {time_taken:.4f} seconds")
            print(f"Total CPU cycles ran: {cpu_cycles:.4f}")
        else:
            print("No valid counterfactual found within the specified number of generations.")
            print("Try increasing the number of generations or population size and/or altering alpha, beta and/or perturbation_fraction. As a last resort, you can also try changing the seed.")
        print("------ End of Results ------\n")

    def __str__(self):
        """
        Return a string representation of the Utility object.

        @return: String representation of the Utility object.
        @rtype: str
        """
        predict_fn_name = self.predict_fn.__name__ if self.predict_fn else self.predict_fn
        return f"Utility Object:\n" \
               f"Data Instance: {self.data_instance}\n" \
               f"Categories: {self.categories}\n" \
               f"Immutable Features: {self.immutable_features}\n" \
               f"Target Class: {self.target_class}\n" \
               f"Verbose: {self.verbose}\n" \
               f"Predict Function: {predict_fn_name}\n" \
               f"Disagreement Object: {self.disagreement}\n" \
               f"Base Counterfactuals: {self.base_counterfactuals}\n" \
               f"Labels: {self.labels}\n"
    
    def to_string(self):
        """
        Return a string representation of the Utility object.

        @return: String representation of the Utility object.
        @rtype: str
        """
        return str(self)
    
    def compute_disagreement_matrix(self, counterfactuals, agreement):
        """
        Compute the disagreement matrix between counterfactuals.

        @param counterfactuals: The list of counterfactuals for which the disagreement matrix is computed.
        @type counterfactuals: list of list

        @param agreement: Boolean flag to compute the agreement matrix instead of disagreement matrix.
        @type agreement: bool

        @return: The disagreement matrix or agreement matrix.
        @rtype: numpy.ndarray
        """
        n = len(counterfactuals)
        disagreement_matrix = np.zeros((n, n), dtype=float)

        for i in range(n):
            for j in range(n):
                disagreement_score = self.disagreement.calculate_disagreement(counterfactuals[i], counterfactuals[j])
                if agreement:
                    disagreement_score = 1 - disagreement_score
                disagreement_matrix[i, j] = disagreement_score
                disagreement_matrix[j, i] = disagreement_score

        return disagreement_matrix
    
    def plot_agreement_heatmap(self, agreement=True, dataset_name=None):
        """
        Plot a heatmap of the agreement or disagreement matrix.

        @param agreement: Boolean flag to plot the agreement heatmap (True) or disagreement heatmap (False).
        @type agreement: bool
        """
        disagreement_matrix = self.compute_disagreement_matrix(self.base_counterfactuals, agreement)
        plt.figure(figsize=(len(self.labels), len(self.labels)))
        sns.heatmap(disagreement_matrix, annot=True, cmap=sns.cubehelix_palette(as_cmap=True), xticklabels=self.labels, yticklabels=self.labels)
        plt.xlabel('Counterfactual')
        plt.ylabel('Counterfactual')

        title = "Pairwise Agreement"

        if(dataset_name != None):
            title += f" for the {dataset_name} Dataset"
        plt.title(title)
        plt.show()