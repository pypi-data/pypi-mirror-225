import numpy as np
import concurrent.futures

class Evaluation:
    """
    Evaluation class for calculating fitness scores of candidate counterfactuals.

    @param alpha: Weight for the average disagreement score.
    @type alpha: float

    @param beta: Weight for the proximity score.
    @type beta: float

    @param predict_proba_fn: The function used for making probability predictions with the model.
    @type predict_proba_fn: callable

    @param instance_probability: The probability of the data_instance belonging to the target class.
    @type instance_probability: float

    @param base_counterfactuals: The base counterfactual instances.
    @type base_counterfactuals: list of list of int

    @param disagreement: The Disagreement object used for calculating disagreement measures.
    @type disagreement: Disagreement

    @param data_instance: The original data instance for which counterfactuals are being generated.
    @type data_instance: list of int

    @param theta: Weight for the misclassification penalty score.
    @type theta: float

    @param gamma: Weight for the sparsity score.
    @type sparsity: float

    @param parallel: A boolean flag indicating whether to run evaluations in parallel (True/False).
    @type parallel: bool

    @param target_class: The target class of the generated meta-counterfactual.
    @type target_class: int
    """
    def __init__(self, alpha, beta, predict_proba_fn, instance_probability, base_counterfactuals, disagreement, data_instance, theta, parallel, gamma, target_class, wachter):
        self.alpha = alpha
        self.beta = beta
        self.predict_proba_fn = predict_proba_fn
        self.instance_probability = instance_probability
        self.base_counterfactuals = base_counterfactuals
        self.disagreement = disagreement
        self.data_instance = data_instance
        self.theta = theta
        self.parallel = parallel
        self.gamma = gamma
        self.target_class = target_class
        self.wachter = wachter

    def __str__(self):
        """
        Return a string representation of the Evaluation object.

        @return: String representation of the Evaluation object.
        @rtype: str
        """
        predict_proba_fn_name = self.predict_proba_fn.__name__ if callable(self.predict_proba_fn) else self.predict_proba_fn

        return f"Evaluation Object:\n" \
               f"Alpha: {self.alpha}\n" \
               f"Beta: {self.beta}\n" \
               f"Predict Proba Function Name: {predict_proba_fn_name}\n" \
               f"Instance Probability: {self.instance_probability}\n" \
               f"Base Counterfactuals: {self.base_counterfactuals}\n" \
               f"Disagreement Object:\n {self.disagreement.to_string()}" \
               f"Data Instance: {self.data_instance}\n" \
               f"Theta: {self.theta}\n" \
               f"Gamma: {self.gamma}\n" \
               f"Parallel: {self.parallel}\n"
   
    def to_string(self):
        """
        Return a string representation of the Evaluation object.

        @return: String representation of the Evaluation object.
        @rtype: str
        """
        return self.__str__()

    def calculate_base_cf_scores(self, population, base_cf):
        """
        Calculate the average disagreement score between candidate instances and a base counterfactual.

        @param population: List of candidate instances.
        @type population: list of list of int

        @param base_cf: The base counterfactual instance.
        @type base_cf: list of int

        @return: The average disagreement score.
        @rtype: float
        """
        base_cf_scores = []

        if self.parallel:
            # Use ThreadPoolExecutor to compute agreement scores in parallel
            with concurrent.futures.ThreadPoolExecutor() as executor:
                agreement_scores = list(executor.map(self.calculate_agreement_score, population, [base_cf] * len(population)))

            base_cf_scores = agreement_scores  # Store the agreement scores in the base_cf_scores list
        else:
            for candidate_instance in population:
                agreement_score = self.calculate_agreement_score(candidate_instance, base_cf)
                base_cf_scores.append(agreement_score)

        return sum(base_cf_scores) / len(base_cf_scores)

    def calculate_agreement_score(self, candidate_instance, base_cf):
        """
        Calculate the disagreement score between a candidate instance and a base counterfactual.

        @param candidate_instance: The candidate instance.
        @type candidate_instance: list of int

        @param base_cf: The base counterfactual instance.
        @type base_cf: list of int

        @return: The disagreement score.
        @rtype: float
        """
        agreement_score = self.disagreement.calculate_disagreement(candidate_instance, base_cf)
        return agreement_score

    def calculate_combined_fitness(self, candidate_instance, base_cf_scores):
        """
        Calculate the combined fitness score of a candidate instance.

        @param candidate_instance: The candidate instance.
        @type candidate_instance: list of int

        @param base_cf_scores: List of average disagreement scores for each base counterfactual.
        @type base_cf_scores: list of float

        @return: The combined fitness score.
        @rtype: float
        """
        combined_fitness = float('inf')

        if(self.wachter == True):
            penalty = self.misclassification_penalty_wachter(candidate_instance)
            proximity_score = self.disagreement.calculate_proximity(self.data_instance, candidate_instance, True)

            combined_fitness = (0.8 * proximity_score) + (0.2 * penalty)
        else:
            avg_disagreement = sum(score for score in base_cf_scores) / len(base_cf_scores)
            proximity_score = self.disagreement.calculate_proximity(self.data_instance, candidate_instance, True)
            sparsity_score, _ = self.disagreement.calculate_sparsity(candidate_instance)
            penalty = self.misclassification_penalty(candidate_instance)
            combined_fitness = (self.alpha * avg_disagreement) + (self.theta * penalty) + (self.beta * proximity_score) + (self.gamma * sparsity_score)
            
        return combined_fitness

    def misclassification_penalty(self, counterfactual):
        """
        Calculate the misclassification penalty score for a counterfactual.

        @param counterfactual: The counterfactual instance.
        @type counterfactual: list of int

        @return: The misclassification penalty score.
        @rtype: float
        """
        probability = self.predict_proba_fn(counterfactual)
        return np.dot(probability, self.instance_probability)
    
    def misclassification_penalty_wachter(self, counterfactual):
        """
        Calculate the Wacther misclassification penalty score for a counterfactual.

        @param counterfactual: The counterfactual instance.
        @type counterfactual: list of int

        @return: The misclassification penalty score.
        @rtype: float
        """
        probability = self.predict_proba_fn(counterfactual)
        probability_target = probability[self.target_class]
        instance_probability_target = self.instance_probability[self.target_class]

        return 1 - abs(probability_target - instance_probability_target)

    def evaluate_population(self, population):
        """
        Evaluate the fitness scores of a population of candidate counterfactuals.

        @param population: List of candidate instances.
        @type population: list of list of int

        @return: List of combined fitness scores for each candidate instance.
        @rtype: list of float
        """
        combined_fitness_scores = []
        base_cf_scores = []
        
        for base_cf in self.base_counterfactuals:
            base_cf_scores.append(self.calculate_base_cf_scores(population, base_cf))

        if self.parallel:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                combined_fitness_scores = list(executor.map(self.calculate_combined_fitness, population, [base_cf_scores] * len(population)))
        else:
            for candidate_instance in population:
                fitness_score = self.calculate_combined_fitness(candidate_instance, base_cf_scores)
                combined_fitness_scores.append(fitness_score)

        return combined_fitness_scores

        